import cv2
import numpy as np
import easyocr
from PIL import Image, ImageEnhance
from pix2tex.cli import LatexOCR

# Initialize models once
easyocr_reader = easyocr.Reader(['en'])
latex_model = LatexOCR()

def preprocess_for_math(image_path):
    """Lane 1: Gentle preprocessing for the deep-learning Math OCR"""
    try:
        # Load as a standard RGB color image
        img = Image.open(image_path).convert('RGB')
        
        # Boost the contrast slightly so faded pencil/ink pops out more, 
        # but keep the smooth edges intact.
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.5) 
        return img
    except Exception as e:
        print(f"Math preprocessing error: {e}")
        return None

def preprocess_for_text(image_path):
    """Lane 2: Heavy-duty B&W preprocessing for EasyOCR"""
    image = cv2.imread(image_path)
    if image is None: 
        return None

    # Upscale, grayscale, blur, and binarize
    image = cv2.resize(image, None, fx=2.0, fy=2.0, interpolation=cv2.INTER_CUBIC)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.bilateralFilter(gray, 9, 75, 75)
    thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    return thresh

def pix2tex_ocr(pil_image):
    if pil_image is None: 
        return ""
    try:
        result = latex_model(pil_image)
        if result and len(result) > 2:
            return result
    except Exception as e:
        print(f"LatexOCR error: {e}")
        pass
    return ""

def easyocr_ocr(processed_cv2_image):
    if processed_cv2_image is None: 
        return ""
    
    results = easyocr_reader.readtext(processed_cv2_image)
    text = ""
    for bbox, detected_text, confidence in results:
        text += detected_text + " "
    return text.strip()

def extract_text_from_image(image_path):
    # 1️⃣ Try math OCR with the gentle color image
    math_img = preprocess_for_math(image_path)
    text = pix2tex_ocr(math_img)

    # 2️⃣ If math OCR fails or misses it, fallback to EasyOCR with the B&W image
    if text == "" or len(text) < 3:
        text_img = preprocess_for_text(image_path)
        text = easyocr_ocr(text_img)

    return text.strip()