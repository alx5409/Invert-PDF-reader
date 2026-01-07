"""
Utility functions for handling PDF files, such as opening, listing, copying, deleting,
renaming, and moving PDF files. Uses PyMuPDF for PDF operations.
"""
import fitz
import logging
import os
from typing import List, Optional

from .file_handler import exists_file_path, exists_folder

PDF_EXTENSION = ".pdf"

def is_pdf_file(file_name: str) -> bool :
    """Check if the file is a PDF based on its extension."""
    return file_name.lower().endswith(PDF_EXTENSION)

def check_pdf_validity(pdf_path: str) -> bool :
    """Check if the PDF file exists and is a valid PDF."""
    if not is_pdf_file(pdf_path):
        logging.error(f"File {pdf_path} is not a supported PDF format")
        return False
    return True

def get_pdf_file(input_folder: str, pdf_filename: str) -> Optional[fitz.Document] :
    """Get a document object by reading a pdf with filename in the input folder"""

    if not exists_folder(input_folder):
        return None
    
    pdf_path = os.path.join(input_folder, pdf_filename)

    if not exists_file_path(pdf_path):
        return None
    
    if not check_pdf_validity(pdf_path):
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
        if is_pdf_file(entry):
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
    
    if not check_pdf_validity(pdf_path):
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
    
    if not check_pdf_validity(pdf_path):
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
    if not check_pdf_validity(src_path):
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

def merge_two_pdf_files(pdf_file_path_1: str, pdf_file_path_2: str, output_folder: str) -> None:
    """Merge two pdf files in one file at the output folder by concateneting the begining of the second into the end of the first."""
    if not exists_file_path(pdf_file_path_1) or not exists_file_path(pdf_file_path_2):
        return
    if not check_pdf_validity(pdf_file_path_1) or not check_pdf_validity(pdf_file_path_2):
        return
    
    if not exists_folder(output_folder):
        return
    
    # Creates the new name of the merged files and checks
    filename_1 = os.path.basename(pdf_file_path_1)
    filename_2 = os.path.basename(pdf_file_path_2)
    new_filename = f"{os.path.splitext(filename_1)[0]}_merge_{os.path.splitext(filename_2)[0]}.pdf"
    new_path = os.path.join(output_folder, new_filename)

    # Joins the two filenames and saves into the ouput folder
    try: 
        pdf_1 = fitz.open(pdf_file_path_1)
        pdf_2 = fitz.open(pdf_file_path_2)
        pdf_1.insert_pdf(pdf_2)
        pdf_1.save(new_path)    
        logging.info(f"Sucess at merging the pdfs {filename_1} and {filename_2} to {new_path}")
    except Exception:
        logging.error(f"Merge of {filename_1} and {filename_2} failed.")
    # Save the pdf in the ouput folder
    finally:
        pdf_1.close()
        pdf_2.close()

def add_page_number_to_pdf(pdf_file_path : str, output_folder: str) -> None:
    """Add page number in the pdf at the bottom right"""
    if not exists_file_path(pdf_file_path):
        return
    
    if not check_pdf_validity(pdf_file_path):
        return
    
    if not exists_folder(output_folder):
        return
    

    try:
        pdf = fitz.open(pdf_file_path)
        page_numbers = range(len(pdf))
        for page_number in page_numbers:
            page = pdf[page_number]
            text = f"{page_number + 1} / {len(pdf)}"    # Format of the page number ouput 
            # Position of the text
            rect = page.rect
            x = rect.x1 - 60
            y = rect.y1 - 20
            page.insert_text((x, y), text, fontsize=12, color=(0, 0, 0))    # Insert the page number with black color
        
        filename = os.path.basename(pdf_file_path)
        name, extension = os.path.splitext(filename)
        new_filename = f"{name}_numbered{extension}"
        output_path = os.path.join(output_folder, new_filename)
        pdf.save(output_path)
        logging.info(f"Added page to {name}")
    except Exception:
        logging.error(f"Failed to add page numbers.")
    finally:
        pdf.close()