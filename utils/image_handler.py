from PIL import Image
import logging
from typing import Optional
import os

from file_handler import exists_file_path, exists_folder

IMG_FORMAT = (".png", ".jpg", ".jpeg", ".bmp", ".gif")

def get_img_file(input_folder: str, pdf_filename: str) -> Optional[Image.Image] :
    """Get an image object by reading an image with filename in the input folder"""

    if not exists_folder(input_folder):
        return None
    
    img_path = os.path.join(input_folder, pdf_filename)

    if not exists_file_path(img_path):
        return None
    
    if not img_path.lower().endswith(IMG_FORMAT):
        logging.error(f"File {img_path} is not a supported image format")
        return None
    
    try:
        return Image.open(img_path)
    except Exception as e:
        logging.error(f"Failed to open PDF: {e}")

def get_img_files(input_folder: str) -> Optional[Image.Image] :
    """List all image files in the input folder."""
    img_files = []
    
    if not exists_folder(input_folder):
        return img_files
    
    if not os.listdir(input_folder):
        logging.error(f"Folder {input_folder} is empty")
        return img_files
    
    for entry in os.listdir(input_folder):
        if entry.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif")):
            img_files.append(os.path.join(input_folder, entry))

    logging.info(f"Success at getting files from {input_folder}")
    return img_files