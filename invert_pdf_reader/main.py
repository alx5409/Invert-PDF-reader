from dotenv import load_dotenv
import logging
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from inverter import ImageInverter, PDFInverter

load_dotenv()

# img_filename = os.getenv("IMG_FILENAME")
pdf_filename = os.getenv("PDF_FILENAME")

def main():
    try:
        PDFInverter.invert_pdf(pdf_filename)
    except Exception as e:
        logging.error(f"An error occurred during PDF inversion: {e}")
if __name__ == "__main__":
    main()
