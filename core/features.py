import numpy as np
from scipy.spatial import distance
import cv2
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import (BREAK_STD_DEV_THRESHOLD, BRANCH_DETECTION_RADIUS, 
                    THICKNESS_SAMPLE_POINTS, MAX_THICKNESS_SEARCH,
                    THICKNESS_DEEP_THRESHOLD, THICKNESS_MEDIUM_THRESHOLD,
                    CURVATURE_WAVY_OVERALL, CURVATURE_WAVY_LOCAL,
                    CURVATURE_CURVED_OVERALL, CURVATURE_CURVED_LOCAL)
from utils import calculate_line_length


class FeatureExtractor:
    @staticmethod
    def calculate_curvature_improved(keypoints):
        '''Improved curvature calculation'''
        if len(keypoints) < 3:
            return 0, 0
        
        actual_length = calculate_line_length(keypoints)
        straight_distance = distance.euclidean(keypoints[0], keypoints[-1])
        
        if straight_distance == 0:
            return 0, 0
        
        overall_curvature = (actual_length - straight_distance) / straight_distance
        
        angles = []
        for i in range(1, len(keypoints) - 1):
            vec1 = np.array(keypoints[i]) - np.array(keypoints[i-1])
            vec2 = np.array(keypoints[i+1]) - np.array(keypoints[i])
            norm1 = np.linalg.norm(vec1)
            norm2 = np.linalg.norm(vec2)
            
            if norm1 > 0 and norm2 > 0:
                cos_angle = np.clip(np.dot(vec1, vec2) / (norm1 * norm2), -1.0, 1.0)
                angle = np.arccos(cos_angle)
                angles.append(np.degrees(angle))
        
        max_local_curvature = max(angles) if angles else 0
        return overall_curvature, max_local_curvature

    @staticmethod
    def detect_breaks_adaptive(keypoints):
        '''Adaptive break detection'''
        if len(keypoints) < 2:
            return 0, []
        
        gaps = []
        for i in range(len(keypoints) - 1):
            gap = distance.euclidean(keypoints[i], keypoints[i+1])
            gaps.append(gap)
        
        if not gaps:
            return 0, []
        
        median_gap = np.median(gaps)
        std_gap = np.std(gaps)
        break_threshold = median_gap + BREAK_STD_DEV_THRESHOLD * std_gap
        
        breaks = []
        for i, gap in enumerate(gaps):
            if gap > break_threshold:
                breaks.append(i)
        
        return len(breaks), breaks

    @staticmethod
    def detect_actual_branches(keypoints, img, radius=BRANCH_DETECTION_RADIUS):
        '''Detect actual branches/forks'''
        if len(keypoints) < 3:
            return {'upward': 0, 'downward': 0, 'forks': 0}
        
        branches = {'upward': 0, 'downward': 0, 'forks': 0}
        
        for i in range(1, len(keypoints) - 1):
            x, y = int(keypoints[i][0]), int(keypoints[i][1])
            
            if x < radius or y < radius or x >= img.shape[1] - radius or y >= img.shape[0] - radius:
                continue
            
            roi = img[y-radius:y+radius, x-radius:x+radius]
            if len(roi.shape) == 3:
                roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            
            _, binary = cv2.threshold(roi, 127, 255, cv2.THRESH_BINARY)
            num_labels, labels = cv2.connectedComponents(binary)
            
            if num_labels > 2:
                branches['forks'] += 1
            
            if i < len(keypoints) - 2:
                y_trend = keypoints[i+1][1] - keypoints[i][1]
                if y_trend < -5:
                    branches['upward'] += 1
                elif y_trend > 5:
                    branches['downward'] += 1
        
        return branches

    @staticmethod
    def calculate_line_thickness(keypoints, img, sample_points=THICKNESS_SAMPLE_POINTS):
        '''Calculate average line thickness'''
        if len(keypoints) < 2:
            return 1
        
        thicknesses = []
        indices = np.linspace(0, len(keypoints)-1, min(sample_points, len(keypoints)), dtype=int)
        
        for idx in indices:
            if idx >= len(keypoints) - 1:
                continue
            
            vec = np.array(keypoints[min(idx+1, len(keypoints)-1)]) - np.array(keypoints[idx])
            vec_len = np.linalg.norm(vec)
            
            if vec_len == 0:
                continue
            
            perp = np.array([-vec[1], vec[0]]) / vec_len
            center = keypoints[idx]
            thickness = 0
            
            for dist in range(1, MAX_THICKNESS_SEARCH):
                sample_pos = center + perp * dist
                x, y = int(sample_pos[0]), int(sample_pos[1])
                
                if x < 0 or y < 0 or x >= img.shape[1] or y >= img.shape[0]:
                    break
                
                if len(img.shape) == 3:
                    pixel_val = cv2.cvtColor(img[y:y+1, x:x+1], cv2.COLOR_BGR2GRAY)[0, 0]
                else:
                    pixel_val = img[y, x]
                
                if pixel_val < 128:
                    thickness += 1
                else:
                    break
            
            thicknesses.append(thickness * 2)
        
        return np.mean(thicknesses) if thicknesses else 1

    @staticmethod
    def classify_thickness(thickness):
        '''Classify line thickness'''
        if thickness > THICKNESS_DEEP_THRESHOLD:
            return 'deep'
        elif thickness > THICKNESS_MEDIUM_THRESHOLD:
            return 'medium'
        else:
            return 'faint'

    @staticmethod
    def classify_curvature_improved(overall_curvature, max_local_curvature):
        '''Improved curvature classification'''
        if max_local_curvature > CURVATURE_WAVY_LOCAL or overall_curvature > CURVATURE_WAVY_OVERALL:
            return 'wavy'
        elif overall_curvature > CURVATURE_CURVED_OVERALL or max_local_curvature > CURVATURE_CURVED_LOCAL:
            return 'curved'
        else:
            return 'straight'

    @staticmethod
    def extract_features_improved(keypoints, img):
        '''Extract all features with improved methods'''
        features = {}
        
        try:
            length = calculate_line_length(keypoints)
            features['length'] = length
            
            overall_curv, max_local_curv = FeatureExtractor.calculate_curvature_improved(keypoints)
            features['curvature_ratio'] = overall_curv
            features['max_local_curvature'] = max_local_curv
            features['curvature'] = FeatureExtractor.classify_curvature_improved(overall_curv, max_local_curv)
            
            num_breaks, break_positions = FeatureExtractor.detect_breaks_adaptive(keypoints)
            features['breaks'] = num_breaks
            features['break_positions'] = break_positions
            
            branches = FeatureExtractor.detect_actual_branches(keypoints, img)
            features['branches'] = branches
            
            thickness = FeatureExtractor.calculate_line_thickness(keypoints, img)
            features['thickness'] = thickness
            features['depth'] = FeatureExtractor.classify_thickness(thickness)
            
            features['start_point'] = tuple(keypoints[0])
            features['end_point'] = tuple(keypoints[-1])
            
        except Exception as e:
            print(f"Error in feature extraction: {e}")
            features = {
                'length': 0, 'length_class': 'unknown',
                'curvature': 'unknown', 'breaks': 0,
                'branches': {'upward': 0, 'downward': 0, 'forks': 0},
                'depth': 'medium'
            }
        
        return features