"""File handling utilities for copying, deleting, pasting, and renaming text files and transform to PDF."""
import logging
import os
from typing import Optional

TEXT_EXTENSION = ".txt"

def is_text_file(file_name: str) -> bool :
    """Check if the file is a text file based on its extension."""
    return file_name.lower().endswith(TEXT_EXTENSION)

def check_text_validity(text_path: str) -> bool :
    """Check if the text file exists and is a valid text file."""
    if not is_text_file(text_path):
        logging.error(f"File {text_path} is not a supported text format")
        return False
    return True

def read_text_file(text_path: str) -> str :
    """Read and return the content of a text file."""
    content = ""
    if not check_text_validity(text_path):
        return content
    
    try:
        with open(text_path, 'r', encoding='utf-8') as file:
            content = file.read()
            logging.info(f"Successfully read text file {text_path}")
            return content
    except Exception as e:
        logging.error(f"Failed to read text file {text_path}: {e}")
        return content
    
def delete_text_file(text_path: str) -> bool :
    """Delete a text file."""
    if not check_text_validity(text_path):
        return False
    
    try:
        os.remove(text_path)
        logging.info(f"Successfully deleted text file {text_path}")
        return True
    except Exception as e:
        logging.error(f"Failed to delete text file {text_path}: {e}")
        return False
    
def rename_text_file(old_path: str, new_path: str) -> bool :
    """Rename a text file."""
    if not check_text_validity(old_path):
        return False
    
    try:
        os.rename(old_path, new_path)
        logging.info(f"Successfully renamed text file from {old_path} to {new_path}")
        return True
    except Exception as e:
        logging.error(f"Failed to rename text file {old_path}: {e}")
        return False