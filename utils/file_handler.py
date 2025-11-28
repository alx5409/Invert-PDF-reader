import os
import fitz
import logging
from typing import List, Optional

def get_pdf_file(input_folder: str, pdf_filename: str) -> Optional[fitz.Document] :
    """Get a document object by reading a pdf with filename in the input folder"""

    if not os.path.exists(input_folder):
        logging.error(f"Folder {input_folder} does not exist")
        return None
    
    pdf_path = os.path.join(input_folder, pdf_filename)

    if not os.path.exists(pdf_path):
        logging.error(f"File with path name {pdf_path} does not exist")
        return None
    
    try:
        return fitz.open(pdf_path)
    except Exception as e:
        logging.error(f"Failed to open PDF: {e}")
    

def get_pdf_files(input_folder: str) -> List[str] :
    """List all PDF files in the input folder."""
    pdf_files = []
    
    if not os.path.exists(input_folder):
        logging.error(f"Folder {input_folder} does not exist")
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

    if not os.path.exists(output_folder):
        logging.error(f"Folder {output_folder} does not exist")
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

# TODO
# Remove pdf file from a folder
def delete_pdf_file(pdf_path: str) -> None:
    """Delete a PDF file if it exists."""
    pass

# Rename a PDF in a folder
def rename_pdf_file(old_path: str, new_path: str) -> None:
    """Rename a PDF file."""
    pass

# Move a pdf file from one folder to another
def move_pdf_file(src_path: str, dest_folder: str) -> None:
    """Move a PDF file to another folder."""
    pass

# Move all pdf files from one folder to another
def move_all_pdf_files(src_folder: str, dest_folder: str) -> None:
    """Move all PDF files from one folder to another."""
    pass