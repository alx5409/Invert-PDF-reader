"""Utility functions for handling image files, such as opening, listing, copying, deleting,
renaming, and converting images to PDF files."""

import logging
from PIL import Image
import os
from typing import Optional

from .file_handler import exists_file_path, exists_folder
from .pdf_handler import is_pdf_file

IMG_EXTENSIONS   = (".png", ".jpg", ".jpeg", ".bmp", ".gif")

def is_img_file(file_name: str) -> bool :
    """Check if the file is an image based on its extension."""
    return file_name.lower().endswith(IMG_EXTENSIONS)

def get_img_file(input_folder: str, img_filename: str) -> Optional[Image.Image] :
    """Get an image object by reading an image with filename in the input folder"""

    if not exists_folder(input_folder):
        return None
    
    img_path = os.path.join(input_folder, img_filename)

    if not exists_file_path(img_path):
        return None
    
    if not is_img_file(img_path):
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
    
    try:
        for entry in os.listdir(input_folder):
            if is_img_file(entry):
                img_files.append(os.path.join(input_folder, entry))

        logging.info(f"Success at getting files from {input_folder}")
    except Exception as e:
        logging.error(f"Failed to get image files from {input_folder}: {e}")
    return img_files

def copy_img_to_output(img_file: Image.Image, input_path: str, output_folder:str) -> None :
    """Copies a single image file in the output folder with a new name"""

    if not exists_folder(output_folder):
        return
    
    if not img_file:
        logging.error(f"Image file was not provided")
        return
    
    try:
        filename = os.path.basename(input_path)
        name, extension = os.path.splitext(filename)
        new_name = f"{name}_(copy){extension}"
        output_path = os.path.join(output_folder, new_name)
        img_file.save(output_path)
        logging.info(f"Success at copying {new_name} to {output_folder}")
    except Exception as e:
        logging.error(f"Failed to copy image file to {output_folder}: {e}")
        return
    
def delete_img_file(img_path: str) -> None:
    """Delete an image file if it exists."""
    if not exists_file_path(img_path):
        return
    
    if not is_img_file(img_path):
        logging.error(f"File {img_path} is not a supported image format")
        return
    
    try:
        os.remove(img_path)
        logging.info(f"Deleted image file: {img_path}")
    except Exception as e:
        logging.error(f"Failed to delete image file {img_path}: {e}")

def rename_img_file(old_path: str, new_name: str) -> None:
    """Rename an image file to a new name in the same directory."""
    if not exists_file_path(old_path):
        return
    
    if not is_img_file(old_path):
        logging.error(f"File {old_path} is not a supported image format")
        return
    
    try:
        directory = os.path.dirname(old_path)
        extension = os.path.splitext(old_path)[1]
        new_path = os.path.join(directory, f"{new_name}{extension}")
        os.rename(old_path, new_path)
        logging.info(f"Renamed image file from {old_path} to {new_path}")
    except Exception as e:
        logging.error(f"Failed to rename image file {old_path} to {new_name}: {e}")

def save_image_as_pdf(img: Image.Image, output_pdf_path: str) -> None:
    """Save an image as a PDF file."""
    if not img:
        logging.error("No image provided to save as PDF")
        return
    if not is_pdf_file(output_pdf_path):
        logging.error(f"Output path {output_pdf_path} is not a valid PDF file")
        return
    
    try:
        img.convert('RGB').save(output_pdf_path, "PDF")
        logging.info(f"Saved image as PDF: {output_pdf_path}")
    except Exception as e:
        logging.error(f"Failed to save image as PDF {output_pdf_path}: {e}")