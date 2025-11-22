import cv2
import mediapipe as mp
from ultralytics import YOLO
import numpy as np
from scipy.spatial import distance
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import MOUNT_LANDMARK_MAP, ROTATION_MAP, ROTATION_ANGLES, MEDIAPIPE_DETECTION_CONFIDENCE
from utils import get_pixel_coords

class HandDetector:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        
    def get_landmarks(self, img_rgb, confidence=0.5):
        '''Extract hand landmarks from RGB image'''
        hands = self.mp_hands.Hands(
            static_image_mode=True,
            max_num_hands=1,
            min_detection_confidence=confidence
        )
        results = hands.process(img_rgb)
        hands.close()
        
        if results.multi_hand_landmarks:
            return results.multi_hand_landmarks[0]
        return None

    def extract_mounts(self, hand_landmarks, image_width, image_height):
        '''Extract mount positions from MediaPipe landmarks'''
        mounts = {}
        landmarks_px = []
        
        for lm in hand_landmarks.landmark:
            x_px = int(lm.x * image_width)
            y_px = int(lm.y * image_height)
            landmarks_px.append([x_px, y_px])
        
        mounts['wrist'] = np.array(landmarks_px[MOUNT_LANDMARK_MAP['wrist']])
        mounts['mount_venus'] = np.array(landmarks_px[MOUNT_LANDMARK_MAP['thumb_base']])
        mounts['mount_jupiter'] = np.array(landmarks_px[MOUNT_LANDMARK_MAP['index_base']])
        mounts['mount_saturn'] = np.array(landmarks_px[MOUNT_LANDMARK_MAP['middle_base']])
        mounts['mount_apollo'] = np.array(landmarks_px[MOUNT_LANDMARK_MAP['ring_base']])
        mounts['mount_mercury'] = np.array(landmarks_px[MOUNT_LANDMARK_MAP['pinky_base']])
        
        moon_x = mounts['wrist'][0] + (mounts['mount_mercury'][0] - mounts['wrist'][0]) * 0.7
        moon_y = mounts['wrist'][1] - (mounts['wrist'][1] - mounts['mount_mercury'][1]) * 0.3
        mounts['mount_moon'] = np.array([moon_x, moon_y])
        
        palm_width = distance.euclidean(mounts['mount_venus'], mounts['mount_mercury'])
        palm_length = distance.euclidean(mounts['wrist'], mounts['mount_saturn'])
        mounts['palm_width'] = palm_width
        mounts['palm_length'] = palm_length
        
        return mounts
    
    def detect_and_rotate_to_portrait(self, img):
        '''Detect hand orientation and rotate image to portrait with hand upright'''
        h, w = img.shape[:2]
        
        # If already portrait, check if rotation needed
        if h > w:
            print(f"Image is portrait ({w}x{h}), checking orientation...")
        else:
            print(f"Image is landscape ({w}x{h}), detecting hand orientation...")
        
        # Try all 4 rotations and pick the one where hand is most upright
        best_rotation = 0
        best_score = -1
        
        hands_detector = self.mp_hands.Hands(
            static_image_mode=True,
            max_num_hands=1,
            min_detection_confidence=MEDIAPIPE_DETECTION_CONFIDENCE
        )
        
        rotation_codes = [
            None,  # 0 degrees (no rotation)
            cv2.ROTATE_90_CLOCKWISE,  # 90 degrees
            cv2.ROTATE_180,  # 180 degrees
            cv2.ROTATE_90_COUNTERCLOCKWISE  # 270 degrees
        ]
        
        for angle, rotate_code in zip(ROTATION_ANGLES, rotation_codes):
            # Rotate image
            if rotate_code is None:
                test_img = img.copy()
            else:
                test_img = cv2.rotate(img, rotate_code)
            
            # Test if hand is detected and upright
            test_rgb = cv2.cvtColor(test_img, cv2.COLOR_BGR2RGB)
            results = hands_detector.process(test_rgb)
            
            if results.multi_hand_landmarks:
                landmarks = results.multi_hand_landmarks[0]
                
                # Calculate uprightness score based on wrist (0) to middle finger tip (12)
                wrist = landmarks.landmark[0]
                middle_tip = landmarks.landmark[12]
                
                # Score: vertical distance (positive = finger above wrist)
                vertical_distance = wrist.y - middle_tip.y
                
                # Also check palm orientation
                index_base = landmarks.landmark[5]
                pinky_base = landmarks.landmark[17]
                
                palm_center_y = (index_base.y + pinky_base.y) / 2
                palm_upright_score = wrist.y - palm_center_y
                
                # Combined score
                score = vertical_distance + palm_upright_score
                
                print(f"  Rotation {angle}°: score={score:.4f}")
                
                if score > best_score:
                    best_score = score
                    best_rotation = angle
        
        hands_detector.close()
        
        # Apply best rotation
        if best_rotation == 0:
            print("No rotation needed")
            return img, 0
        elif best_rotation == 90:
            print("Rotating 90° clockwise to portrait")
            return cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE), 90
        elif best_rotation == 180:
            print("Rotating 180°")
            return cv2.rotate(img, cv2.ROTATE_180), 180
        elif best_rotation == 270:
            print("Rotating 90° counter-clockwise to portrait")
            return cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE), 270
        
        return img, 0
    
    def draw_landmarks(self, img, hand_landmarks):
        '''Draw hand landmarks on image'''
        self.mp_drawing.draw_landmarks(
            img,
            hand_landmarks,
            self.mp_hands.HAND_CONNECTIONS,
            self.mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
            self.mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2)
        )
        
    def draw_mounts(self, img, mounts):
        '''Draw mount positions on image'''
        for mount_name, mount_pos in mounts.items():
            if mount_name not in ['palm_width', 'palm_length']:
                cv2.circle(img, tuple(mount_pos.astype(int)), 5, (255, 0, 255), -1)
                cv2.putText(img, mount_name.replace('mount_', ''), 
                           tuple(mount_pos.astype(int) + [10, -10]),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 0, 255), 1)


class LineDetector:
    def __init__(self, model_path):
        self.model = YOLO(model_path)
    
    def detect(self, image_path, conf=0.3, iou=0.4):
        '''Detect palm lines using YOLO'''
        results = self.model.predict(
            source=image_path,
            conf=conf,
            iou=iou,
            save=False
        )
        return results[0] if results else None