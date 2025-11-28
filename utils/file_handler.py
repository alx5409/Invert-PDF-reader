import os
import fitz
import logging

# Get a document object by reading a pdf with filename in the input folder
def get_pdf_file(input_folder: str, pdf_filename: str) -> None :

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
    

# List all PDF files in the input folder
def get_pdf_files(input_folder: str) -> list :
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

    logging.info(f"sucess at getting files from {input_folder}")
    return pdf_files

# Copies a single pdf file in the output folder
def copy_pdf_to_output(pdf_file: fitz.Document, output_folder:str) -> None :

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
    logging.info(f"sucess at copying {pdf_file} in {output_folder}")