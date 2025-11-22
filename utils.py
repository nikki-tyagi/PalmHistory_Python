import numpy as np
from scipy.spatial import distance
from typing import Tuple

def calculate_line_length(keypoints: np.ndarray) -> float:
    '''Calculate total length of line from keypoints'''
    if len(keypoints) < 2:
        return 0.0
    
    total_length = 0.0
    for i in range(len(keypoints) - 1):
        total_length += distance.euclidean(keypoints[i], keypoints[i+1])
    return total_length

def get_pixel_coords(landmark, width: int, height: int) -> np.ndarray:
    '''Converts normalized landmark to pixel coordinates'''
    return np.array([int(landmark.x * width), int(landmark.y * height)])