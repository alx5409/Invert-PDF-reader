"""
General file and folder utility functions for existence checks.
"""

import os
import fitz
import logging
from typing import List, Optional

def exists_file_path(path_file: str)    -> bool :
    if not os.path.exists(path_file):
        logging.error(f"File with path name {path_file} does not exist")
        return False
    
    return True

def exists_folder(path_folder: str) -> bool :
    if not os.path.exists(path_folder):
        logging.error(f"Folder {path_folder} does not exist")
        return False
    
    return True