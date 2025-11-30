from dotenv import load_dotenv
import os

from invert_pdf_reader.inverter import invert_png_file

load_dotenv()

img_filename = os.getenv("IMG_FILENAME")

def main():
    invert_png_file(img_filename)

if __name__ == "__main__":
    main()
