"""
Utility functions for handling files, particularly PDF files. Includes functions to:
-check for file and folder existence
-retrieve PDF files
-copy
-delete
-rename
-move PDF files.
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

def get_pdf_file(input_folder: str, pdf_filename: str) -> Optional[fitz.Document] :
    """Get a document object by reading a pdf with filename in the input folder"""

    if not exists_folder(input_folder):
        return None
    
    pdf_path = os.path.join(input_folder, pdf_filename)

    if not exists_file_path(pdf_path):
        return None
    
    try:
        return fitz.open(pdf_path)
    except Exception as e:
        logging.error(f"Failed to open PDF: {e}")
    

def get_pdf_files(input_folder: str) -> List[str] :
    """List all PDF files in the input folder."""
    pdf_files = []
    
    if not exists_folder(input_folder):
        return pdf_files
    
    if not os.listdir(input_folder):
        logging.error(f"Folder {input_folder} is empty")
        return pdf_files
    
    for entry in os.listdir(input_folder):
        if entry.lower().endswith(".pdf"):
            pdf_files.append(os.path.join(input_folder, entry))

    logging.info(f"Success at getting files from {input_folder}")
    return pdf_files

def copy_pdf_to_output(pdf_file: fitz.Document, output_folder:str) -> None :
    """Copies a single pdf file in the output folder with a new name"""

    if not exists_folder(output_folder):
        return
    
    if not pdf_file:
        logging.error(f"Pdf file was not provided")
        return
    
    original_path = pdf_file.name
    filename : str = os.path.basename(original_path)
    name, extension = os.path.splitext(filename)
    new_filename = f"{name}_(copy){extension}"
    output_path = os.path.join(output_folder, new_filename)
    pdf_file.save(output_path)
    logging.info(f"Success at copying {pdf_file} to {output_folder}")

def delete_pdf_file(pdf_path: str) -> None:
    """Delete a PDF file if it exists."""
    if not exists_file_path(pdf_path):
        return
    
    try:
        os.remove(pdf_path)
        logging.info(f"Deleted PDF file: {pdf_path}")
    except Exception as e:
        logging.error(f"Failed to delete PDF file {pdf_path}")


def rename_pdf_file(pdf_path: str, new_name: str) -> None:
    """Rename a PDF file."""
    if not exists_file_path(pdf_path):
        return
    
    try:
        dir_name = os.path.dirname(pdf_path)
        name = os.path.basename(pdf_path)
        new_path = os.path.join(dir_name, new_name)
        os.rename(pdf_path, new_path)
        logging.info(f"Renamed PDF file from {name} to {new_name}")
    except Exception as e:
        logging.error(f"Failed to rename PDF file {pdf_path}")
    

def move_pdf_file(src_path: str, dest_folder: str) -> None:
    """Move a PDF file to another folder."""
    if not exists_file_path(src_path):
        return
    if not exists_folder(dest_folder):
        return
    if not src_path.lower().endswith('.pdf'):
        logging.error(f"Source path {src_path} is not a PDF file")
        return
    try:
        filename = os.path.basename(src_path)
        dest_path = os.path.join(dest_folder, filename)
        os.rename(src_path, dest_path)
        logging.info(f"Moved PDF file from {src_path} to {dest_folder}")
    except FileNotFoundError:
        logging.error(f"File not found: {src_path}")
    except PermissionError:
        logging.error(f"Permission denied when moving {src_path} to {dest_folder}")
    except OSError as e:
        logging.error(f"OS error when moving {src_path} to {dest_folder}: {e}")

def move_all_pdf_files(src_folder: str, dest_folder: str) -> None:
    """Move all PDF files from one folder to another."""
    if not exists_folder(src_folder):
        return
    if not exists_folder(dest_folder):
        return
    for filename in os.listdir(src_folder):
        file_path = os.path.join(src_folder, filename)
        move_pdf_file(file_path, dest_folder)