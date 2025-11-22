import cv2
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from pipeline import PalmReadingPipeline
from logging_config import logger


def process_palm_reading(image_path, yolo_model_path, output_path='palm_reading_result.jpg'):
    '''Main function to process palm reading'''
    
    try:
        logger.info(f"Starting palm reading analysis for: {image_path}")
        pipeline = PalmReadingPipeline(yolo_model_path)
        result_img, interpretations, mounts = pipeline.process(image_path)
        
        if result_img is not None:
            # Save result
            cv2.imwrite(output_path, result_img)
            logger.info(f"Result saved to: {output_path}")
            
            # Display in Colab
            try:
                from google.colab.patches import cv2_imshow
                cv2_imshow(result_img)
            except:
                cv2.imshow('Palm Reading Result', result_img)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
            
            # Print analysis
            logger.info("=" * 60)
            logger.info("PALM READING ANALYSIS (Vedic Palmistry)")
            logger.info("=" * 60)
            
            logger.info("DETECTED MOUNTS:")
            for mount_name, mount_pos in mounts.items():
                if mount_name not in ['palm_width', 'palm_length']:
                    logger.debug(f"{mount_name}: {mount_pos}")
            logger.info(f"Palm dimensions: {mounts['palm_width']:.1f}px × {mounts['palm_length']:.1f}px")
            
            for line_name, data in interpretations.items():
                logger.info(f"\n{line_name.upper()}")
                logger.info(f"  Length: {data['features']['length_class']}")
                logger.info(f"  Depth: {data['features'].get('depth', 'unknown')}")
                logger.info(f"  Interpretation: {data['interpretation']}")
            
            return result_img, interpretations, mounts
        else:
            logger.error("Failed to process image")
            return None, None, None
            
    except Exception as e:
        logger.exception(f"Error during palm reading: {e}")
        raise


if __name__ == "__main__":
    IMAGE_PATH = '/home/momonga/Downloads/t5.jpeg'
    MODEL_PATH = '/home/momonga/Documents/PalmReaderPro/best.pt'
    
    if len(sys.argv) > 1:
        IMAGE_PATH = sys.argv[1]
    if len(sys.argv) > 2:
        MODEL_PATH = sys.argv[2]
    
    process_palm_reading(IMAGE_PATH, MODEL_PATH)