"""
General file and folder utility functions for existence checks.
"""

import logging
import os

def exists_file_path(path_file: str) -> bool :
    if not os.path.exists(path_file):
        logging.error(f"File with path name {path_file} does not exist")
        return False
    return True

def exists_folder(path_folder: str) -> bool :
    if not os.path.exists(path_folder):
        logging.error(f"Folder {path_folder} does not exist")
        return False
    return True

def rename_file(old_path: str, new_path: str) -> bool :
    """Rename a file from old_path to new_path."""
    if not exists_file_path(old_path):
        return False
    
    try:
        os.rename(old_path, new_path)
        logging.info(f"Successfully renamed file from {old_path} to {new_path}")
        return True
    except Exception as e:
        logging.error(f"Failed to rename file {old_path}: {e}")
        return False