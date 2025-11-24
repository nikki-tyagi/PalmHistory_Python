import gradio as gr
import cv2
import numpy as np
import tempfile
import os
from pipeline import PalmReadingPipeline

# Load model once
pipeline = PalmReadingPipeline('best.pt')

def analyze_palm(image):
    """Process palm and return results"""
    if image is None:
        return None, "Please upload an image"
    
    # Save to temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as f:
        temp_path = f.name
        cv2.imwrite(temp_path, cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
    
    try:
        # Process
        result_img, interpretations, mounts = pipeline.process(temp_path)
        
        if result_img is None:
            return None, "❌ No hand detected"
        
        # Format text
        text = "🔮 VEDIC PALMISTRY ANALYSIS\n\n"
        
        if interpretations:
            for line_name, data in interpretations.items():
                features = data.get('features', {})
                interp = data.get('interpretation', 'N/A')
                
                text += f"📍 {line_name.upper()}\n"
                text += f"   Length: {features.get('length_class', 'unknown')}\n"
                text += f"   Depth: {features.get('depth', 'unknown')}\n"
                text += f"   {interp}\n\n"
        else:
            text += "⚠️ No interpretations generated"
        
        # Convert BGR to RGB
        result_rgb = cv2.cvtColor(result_img, cv2.COLOR_BGR2RGB)
        
        return result_rgb, text
        
    finally:
        # Clean up
        if os.path.exists(temp_path):
            os.remove(temp_path)

# Create interface
demo = gr.Interface(
    fn=analyze_palm,
    inputs=gr.Image(label="📸 Upload Palm Image"),
    outputs=[
        gr.Image(label="🖐️ Annotated Palm"),
        gr.Textbox(label="📖 Reading", lines=20)
    ],
    title="🔮 PalmReaderPro - AI Vedic Palmistry",
    description="Upload a clear palm image for AI-powered analysis based on Vedic palmistry principles",
    theme="soft"
)

if __name__ == "__main__":
    demo.launch()
