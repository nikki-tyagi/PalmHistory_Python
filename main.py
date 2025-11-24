import cv2
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from pipeline import PalmReadingPipeline
from logging_config import logger


def process_palm_reading(image_path, yolo_model_path, output_dir='results'):
    """Main function to process palm reading with proper output naming"""
    
    try:
        logger.info(f"Starting palm reading analysis for: {image_path}")
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Extract filename without extension and create output path
        base_filename = os.path.splitext(os.path.basename(image_path))[0]
        output_path = os.path.join(output_dir, f"{base_filename}_result.jpg")
        
        # Initialize pipeline and process
        pipeline = PalmReadingPipeline(yolo_model_path)
        result_img, interpretations, mounts = pipeline.process(image_path)
        
        if result_img is not None:
            # Save result with proper naming
            cv2.imwrite(output_path, result_img)
            logger.info(f"Result saved to: {output_path}")
            
            # Print analysis header
            print("\n" + "=" * 70)
            print("PALM READING ANALYSIS (Vedic Palmistry)")
            print("=" * 70)
            
            # Print mounts information
            if mounts:
                print("\nDETECTED MOUNTS:")
                for mount_name, mount_pos in mounts.items():
                    if mount_name not in ['palm_width', 'palm_length']:
                        print(f"  {mount_name}: {mount_pos}")
                
                palm_width = mounts.get('palm_width', 'N/A')
                palm_length = mounts.get('palm_length', 'N/A')
                
                if palm_width != 'N/A' and palm_length != 'N/A':
                    print(f"\nPalm dimensions: {palm_width:.1f}px × {palm_length:.1f}px")
            else:
                print("\n⚠️  No mount data available")
            
            # Print line interpretations
            if interpretations and len(interpretations) > 0:
                print("\n" + "=" * 70)
                print("LINE INTERPRETATIONS:")
                print("=" * 70)
                
                for line_name, data in interpretations.items():
                    print(f"\n📍 {line_name.upper()}")
                    print("-" * 70)
                    
                    # Safely extract features
                    features = data.get('features', {})
                    interpretation = data.get('interpretation', 'No interpretation available')
                    
                    length_class = features.get('length_class', 'unknown')
                    depth = features.get('depth', 'unknown')
                    
                    print(f"  Length Class: {length_class}")
                    print(f"  Depth: {depth}")
                    print(f"\n  Interpretation:")
                    print(f"  {interpretation}")
                
                print("\n" + "=" * 70 + "\n")
            else:
                print("\n⚠️  WARNING: No line interpretations generated!")
                print("   Possible causes:")
                print("   - Lines detected but not classified (check class_name matching)")
                print("   - VedicInterpreter not returning data")
                print("   - YOLO model not detecting keypoints")
                print(f"\n   Debug: interpretations dict = {interpretations}")
            
            return result_img, interpretations, mounts
        else:
            logger.error("Failed to process image - result_img is None")
            print("\n❌ ERROR: Failed to process image")
            return None, None, None
            
    except Exception as e:
        logger.exception(f"Error during palm reading: {e}")
        print(f"\n❌ EXCEPTION: {e}")
        raise


if __name__ == "__main__":
    # Default paths
    IMAGE_PATH = '/home/momonga/Downloads/t2.jpeg'
    MODEL_PATH = '/home/momonga/Documents/PalmReaderPro/best.pt'
    OUTPUT_DIR = 'results'
    
    # Command line argument support
    if len(sys.argv) > 1:
        IMAGE_PATH = sys.argv[1]
    if len(sys.argv) > 2:
        MODEL_PATH = sys.argv[2]
    if len(sys.argv) > 3:
        OUTPUT_DIR = sys.argv[3]
    
    process_palm_reading(IMAGE_PATH, MODEL_PATH, OUTPUT_DIR)
