import cv2
import os
import numpy as np
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.detectors import HandDetector, LineDetector
from core.features import FeatureExtractor
from core.classifiers import MountBasedClassifier
from core.interpreters import VedicInterpreter
from config import YOLO_CONFIDENCE, YOLO_IOU, COLOR_LINES, COLOR_TEXT


class PalmReadingPipeline:
    def __init__(self, yolo_model_path, target_size=1024):
        '''
        Initialize pipeline with image standardization
        
        Args:
            yolo_model_path: Path to YOLO model
            target_size: Standard size for longer edge (default 1024px)
        '''
        print("Initializing Palm Reading Pipeline...")
        self.hand_detector = HandDetector()
        self.line_detector = LineDetector(yolo_model_path)
        self.target_size = target_size
        print(f"Models loaded! Images will be standardized to {target_size}px")
    
    def standardize_image(self, img):
        '''
        Resize image maintaining aspect ratio
        Longer edge = target_size, shorter edge scales proportionally
        '''
        h, w = img.shape[:2]
        
        # Calculate scaling factor
        if h > w:
            scale = self.target_size / h
            new_h, new_w = self.target_size, int(w * scale)
        else:
            scale = self.target_size / w
            new_w, new_h = self.target_size, int(h * scale)
        
        # Resize with high-quality interpolation
        resized = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_LANCZOS4)
        
        print(f"  Standardized: {w}x{h} → {new_w}x{new_h} (scale: {scale:.2f}x)")
        return resized, scale
    
    def process(self, image_path):
        '''Complete pipeline with image standardization and auto-rotation'''
        
        # Load image
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Could not load image: {image_path}")
        
        print(f"Original image size: {img.shape[1]}x{img.shape[0]}")
        
        # STANDARDIZE IMAGE SIZE (NEW!)
        img, scale_factor = self.standardize_image(img)
        
        # Auto-rotate to portrait
        try:
            img, rotation_angle = self.hand_detector.detect_and_rotate_to_portrait(img)
            print(f"Image rotated by {rotation_angle}° for processing")
        except Exception as e:
            print(f"Rotation error: {e}")
            h, w = img.shape[:2]
            if w > h:
                img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
                rotation_angle = 90
            else:
                rotation_angle = 0
        
        # Process image
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        h, w = img.shape[:2]
        
        # Detect hand landmarks
        hand_landmarks = self.hand_detector.get_landmarks(img_rgb)
        
        if not hand_landmarks:
            print("No hand detected by MediaPipe after rotation, trying 180° flip...")
            img = cv2.rotate(img, cv2.ROTATE_180)
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            hand_landmarks = self.hand_detector.get_landmarks(img_rgb)
            
            if not hand_landmarks:
                print("Still no hand detected, returning None")
                return None, None, None
        
        # Extract mounts
        mounts = self.hand_detector.extract_mounts(hand_landmarks, w, h)
        
        # Draw landmarks and mounts
        self.hand_detector.draw_landmarks(img, hand_landmarks)
        self.hand_detector.draw_mounts(img, mounts)
        
        # Save standardized image temporarily for YOLO
        temp_rotated_path = image_path.replace('.jpg', '_standardized_temp.jpg').replace('.png', '_standardized_temp.png')
        cv2.imwrite(temp_rotated_path, img)
        
        # Detect lines on standardized image
        line_result = self.line_detector.detect(temp_rotated_path, conf=YOLO_CONFIDENCE, iou=YOLO_IOU)
        
        # Clean up temp file
        try:
            os.remove(temp_rotated_path)
        except:
            pass
        
        interpretations = {}
        
        if line_result and line_result.keypoints is not None:
            keypoints = line_result.keypoints.xy.cpu().numpy()
            
            if hasattr(line_result, 'boxes') and line_result.boxes is not None:
                class_ids = line_result.boxes.cls.cpu().numpy().astype(int)
            else:
                class_ids = list(range(len(keypoints)))
            
            for i, kpts in enumerate(keypoints):
                valid_kpts = kpts[~np.all(kpts == 0, axis=1)]
                
                if len(valid_kpts) < 2:
                    continue
                
                pts = valid_kpts.astype(np.int32)
                
                class_id = class_ids[i] if i < len(class_ids) else 0
                class_name = self.line_detector.model.names[class_id] if hasattr(self.line_detector.model, 'names') else f"Line_{class_id}"
                
                line_start = valid_kpts[0]
                line_end = valid_kpts[-1]
                
                # Determine line type
                line_type = None
                if 'life' in class_name.lower():
                    line_type = 'life'
                elif 'heart' in class_name.lower():
                    line_type = 'heart'
                elif 'head' in class_name.lower():
                    line_type = 'head'
                elif 'fate' in class_name.lower():
                    line_type = 'fate'
                
                if line_type:
                    # Classify length based on mounts (now on standardized coordinates)
                    length_class = MountBasedClassifier.classify_line_length_by_mounts(
                        line_start, line_end, line_type, mounts
                    )
                    
                    # Extract features
                    features = FeatureExtractor.extract_features_improved(valid_kpts, img)
                    features['length_class'] = length_class
                    
                    # Generate Vedic interpretation
                    if line_type == 'life':
                        interpretation = VedicInterpreter.interpret_life_line_detailed_vedic(features)
                    elif line_type == 'heart':
                        interpretation = VedicInterpreter.interpret_heart_line_detailed_vedic(features)
                    elif line_type == 'head':
                        interpretation = VedicInterpreter.interpret_head_line_detailed_vedic(features)
                    elif line_type == 'fate':
                        interpretation = VedicInterpreter.interpret_fate_line_detailed_vedic(features, present=True)
                    
                    interpretations[class_name] = {
                        'features': features,
                        'interpretation': interpretation
                    }
                    
                    # Draw line on image
                    cv2.polylines(img, [pts], False, COLOR_LINES, 3)
                    
                    label = f"{class_name} ({length_class})"
                    label_x, label_y = int(pts[0][0]), int(pts[0][1]) - 10
                    cv2.putText(img, label, (label_x, label_y),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.6, COLOR_TEXT, 2)
        
        return img, interpretations, mounts