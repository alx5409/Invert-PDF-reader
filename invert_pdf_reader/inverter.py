import fitz 
import logging
from PIL import Image
import os

from configuration import config
import utils

def invert_single_color(color: int) -> int:
    """Inverts a color value based on the maximum color number defined in config."""
    return config.COLOR_NUMBER - color

def invert_image(image: Image.Image) -> Image.Image:
    """Inverts the colors of a PIL Image and returns the inverted image."""
    return Image.eval(image, lambda x: invert_single_color(x))

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
        inverted_image = invert_image(image)
        inverted_image_path = os.path.join(config.OUTPUT_FOLDER, f"inverted_{img_filename}")
        inverted_image.save(inverted_image_path)
        logging.info(f"Inverted image saved to {inverted_image_path}")
    except Exception as e:
        logging.error(f"Failed to invert image {img_filename}: {e}")
        return
    
def invert_pdf(path_file: str) -> None:
    """Inverts the colors of each page in a PDF file and saves it to the output folder."""
    # Get pdf file
    pdf_filename = os.path.basename(path_file)
    pdf_document = utils.pdf_handler.get_pdf_file(config.INPUT_FOLDER, pdf_filename)
    if not pdf_document:
        logging.error(f"Could not read PDF {pdf_filename}")
        return
    
    # Transform pdf pages to images
    images = [page.get_pixmap() for page in pdf_document]
    if not images:
        logging.error(f"No pages found in PDF {pdf_filename}")
        return
    
    # Invert color of each page image
    inverted_images = []
    for img in images:
        pil_image = Image.frombytes("RGB", [img.width, img.height], img.samples)
        inverted_image = Image.eval(pil_image, lambda x: 255 - x)
        inverted_images.append(inverted_image)

    # Merge the images in one file
    try:
        output_pdf_path = os.path.join(config.OUTPUT_FOLDER, f"inverted_{pdf_filename}")
        inverted_images[0].save(output_pdf_path, save_all=True, append_images=inverted_images[1:], format="PDF")
        logging.info(f"Inverted PDF saved to {output_pdf_path}")
    except Exception as e:
        logging.error(f"Failed to save inverted PDF {pdf_filename}: {e}")
        return
    
