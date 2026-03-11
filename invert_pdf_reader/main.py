from dotenv import load_dotenv
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from inverter import ImageInverter, PDFInverter

load_dotenv()

img_filename = os.getenv("IMG_FILENAME")
pdf_filename = os.getenv("PDF_FILENAME")

def main():
    if pdf_filename:
        PDFInverter.invert_pdf(pdf_filename)
    elif img_filename:
        ImageInverter.invert_png_file(img_filename)
    else:
        print("Please set IMG_FILENAME or PDF_FILENAME in .env file")

if __name__ == "__main__":
    main()
