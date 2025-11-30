import fitz 
import logging
from PIL import Image
import os

from configuration import config
import utils


def invert_png_file(path_file: str) -> None:
    """Inverts the colors of a PNG file and saves it to the output folder."""
    # Read image
    img_filename = os.path.basename(path_file)
    image = utils.image_handler.get_img_file(config.INPUT_FOLDER, img_filename)
    if not image:
        logging.error(f"Could not read image {img_filename}")
        return
    
    # Invert colors
    try:
        image = image.convert("RGB")
        inverted_image = Image.eval(image, lambda x: 255 - x)
        inverted_image_path = os.path.join(config.OUTPUT_FOLDER, f"inverted_{img_filename}")
        inverted_image.save(inverted_image_path)
        logging.info(f"Inverted image saved to {inverted_image_path}")
    except Exception as e:
        logging.error(f"Failed to invert image {img_filename}: {e}")
        return
    
def invert_pdf():
    # Get pdf file
    # Transform pdf pages to images
    # Invert color of each page image
    # Merge the images in one file
    # Copy the pdf in the output file
    pass
