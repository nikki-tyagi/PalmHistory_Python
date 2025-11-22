import pytest
import numpy as np
from utils import calculate_line_length, get_pixel_coords


class TestUtils:
    def test_calculate_line_length_empty(self):
        '''Test with no keypoints'''
        assert calculate_line_length(np.array([])) == 0.0
    
    def test_calculate_line_length_single(self):
        '''Test with single point'''
        assert calculate_line_length(np.array([[0, 0]])) == 0.0
    
    def test_calculate_line_length_straight(self):
        '''Test straight horizontal line'''
        points = np.array([[0, 0], [3, 0], [7, 0]])
        assert calculate_line_length(points) == 7.0
    
    def test_calculate_line_length_diagonal(self):
        '''Test diagonal line (3-4-5 triangle)'''
        points = np.array([[0, 0], [3, 4]])
        assert calculate_line_length(points) == 5.0


class TestPixelCoords:
    def test_get_pixel_coords_center(self):
        '''Test landmark at center'''
        class MockLandmark:
            x, y = 0.5, 0.5
        
        result = get_pixel_coords(MockLandmark(), 100, 200)
        assert result[0] == 50
        assert result[1] == 100
    
    def test_get_pixel_coords_corner(self):
        '''Test landmark at corner'''
        class MockLandmark:
            x, y = 1.0, 1.0
        
        result = get_pixel_coords(MockLandmark(), 640, 480)
        assert result[0] == 640
        assert result[1] == 480