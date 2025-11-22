# Vedic Palm Reader AI

Professional palm reading using YOLOv8 and MediaPipe with Vedic interpretations.

## Features
- Auto-rotation and hand detection
- Mount-based classification
- Vedic interpretations
- Modular architecture
- Unit tested

## Installation
Install dependencies:
pip install -r requirements.txt

## Usage
from main import process_palm_reading
result_img, interpretations, mounts = process_palm_reading("palm.jpg", "model.pt")

## License
MIT License
