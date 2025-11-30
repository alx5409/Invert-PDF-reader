#TODO Implement file handling utilities for copying, deleting, pasting, and renaming text files and transform to PDF.
import logging
# import os
# from typing import Optional

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