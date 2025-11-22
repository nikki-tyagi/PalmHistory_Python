import pytest
import numpy as np
from core.classifiers import MountBasedClassifier


class TestMountClassification:
    def setup_method(self):
        '''Setup mock mounts data'''
        self.mounts = {
            'mount_jupiter': np.array([100, 50]),
            'mount_saturn': np.array([150, 50]),
            'mount_apollo': np.array([200, 50]),
            'mount_mercury': np.array([250, 50]),
            'mount_venus': np.array([50, 150]),
            'mount_moon': np.array([250, 150]),
            'wrist': np.array([150, 300]),
            'palm_width': 200.0,
            'palm_length': 250.0
        }
    
    def test_heart_line_long(self):
        '''Test long heart line classification'''
        line_start = np.array([50, 100])
        line_end = np.array([110, 90])  # Near Jupiter
        
        result = MountBasedClassifier.classify_line_length_by_mounts(
            line_start, line_end, 'heart', self.mounts
        )
        assert result == 'long'
    
    def test_heart_line_short(self):
        '''Test short heart line classification'''
        line_start = np.array([50, 100])
        line_end = np.array([220, 90])  # Near Apollo
        
        result = MountBasedClassifier.classify_line_length_by_mounts(
            line_start, line_end, 'heart', self.mounts
        )
        assert result == 'short'
    
    def test_life_line_normalization(self):
        '''Test life line uses normalized ratios'''
        line_start = np.array([100, 100])
        line_end = np.array([80, 280])  # Near wrist
        
        result = MountBasedClassifier.classify_line_length_by_mounts(
            line_start, line_end, 'life', self.mounts
        )
        assert result == 'long'