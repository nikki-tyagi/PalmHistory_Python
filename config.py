import cv2

# MediaPipe Landmark Mapping
MOUNT_LANDMARK_MAP = {
    'wrist': 0,
    'thumb_base': 1,
    'index_base': 5,
    'middle_base': 9,
    'ring_base': 13,
    'pinky_base': 17,
    'thumb_tip': 4,
    'index_tip': 8,
    'middle_tip': 12,
    'ring_tip': 16,
    'pinky_tip': 20
}

# Rotation Mappings
ROTATION_MAP = {
    0: None,
    90: cv2.ROTATE_90_CLOCKWISE,
    180: cv2.ROTATE_180,
    270: cv2.ROTATE_90_COUNTERCLOCKWISE
}

ROTATION_ANGLES = [0, 90, 180, 270]

# Detection Parameters
MEDIAPIPE_DETECTION_CONFIDENCE = 0.3
YOLO_CONFIDENCE = 0.3
YOLO_IOU = 0.4

# Feature Extraction Settings
BREAK_STD_DEV_THRESHOLD = 2.0
BRANCH_DETECTION_RADIUS = 15
THICKNESS_SAMPLE_POINTS = 5
MAX_THICKNESS_SEARCH = 20

# Thickness Classification Thresholds
THICKNESS_DEEP_THRESHOLD = 6
THICKNESS_MEDIUM_THRESHOLD = 3

# Curvature Classification Thresholds
CURVATURE_WAVY_OVERALL = 0.3
CURVATURE_WAVY_LOCAL = 45
CURVATURE_CURVED_OVERALL = 0.1
CURVATURE_CURVED_LOCAL = 20

# Colors (BGR format)
COLOR_LANDMARKS = (0, 255, 0)
COLOR_CONNECTIONS = (255, 0, 0)
COLOR_MOUNTS = (255, 0, 255)
COLOR_LINES = (0, 255, 0)
COLOR_TEXT = (0, 255, 255)