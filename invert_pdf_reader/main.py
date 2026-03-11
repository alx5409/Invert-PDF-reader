from dotenv import load_dotenv
import os

from invert_pdf_reader.inverter import ImageInverter, PDFInverter

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
