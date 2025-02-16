import os
from PyPDF2 import PdfReader
from PIL import Image
import pytesseract
import logging

logger = logging.getLogger(__name__)

def process_uploaded_file(file, file_path):
    """Process uploaded files and extract text content"""
    try:
        file_extension = os.path.splitext(file.name)[1].lower()
        
        # Save the file
        with open(file_path, 'wb') as f:
            f.write(file.getbuffer())
            
        # Extract text based on file type
        if file_extension == '.pdf':
            return extract_text_from_pdf(file_path)
        elif file_extension in ['.png', '.jpg', '.jpeg']:
            return extract_text_from_image(file_path)
        elif file_extension in ['.txt', '.md']:
            return extract_text_from_text(file_path)
        else:
            return f"File {file.name} saved. Content extraction not supported for this file type."
            
    except Exception as e:
        logger.error(f"Error processing file {file.name}: {str(e)}")
        return f"Error processing file {file.name}: {str(e)}"

def extract_text_from_pdf(file_path):
    """Extract text from PDF files"""
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        logger.error(f"Error extracting text from PDF: {str(e)}")
        return f"Error extracting text from PDF: {str(e)}"

def extract_text_from_image(file_path):
    """Extract text from images using OCR"""
    try:
        image = Image.open(file_path)
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        logger.error(f"Error extracting text from image: {str(e)}")
        return f"Error extracting text from image: {str(e)}"

def extract_text_from_text(file_path):
    """Extract text from text files"""
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except Exception as e:
        logger.error(f"Error reading text file: {str(e)}")
        return f"Error reading text file: {str(e)}" 
