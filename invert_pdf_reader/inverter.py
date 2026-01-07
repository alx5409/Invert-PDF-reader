import fitz 
import logging
from PIL import Image
import os

from configuration import config
import utils

class ColorInverter:
    """Handles color inversion logic."""

    @staticmethod
    def invert_single_color(color: int) -> int:
        """Inverts a color value based on the maximum color number defined in config."""
        return config.COLOR_NUMBER - color

    @staticmethod
    def invert_image(image: Image.Image) -> Image.Image:
        """Inverts the colors of a PIL Image and returns the inverted image."""
        return Image.eval(image, lambda x: ColorInverter.invert_single_color(x))
    
class ImageInverter:
    """Handles image inversion logic."""

    @staticmethod
    def save_inverted_image(image: Image.Image, output_path: str) -> None:
        """Saves the inverted image to the specified output path."""
        try:
            image.save(output_path)
            logging.info(f"Inverted image saved to {output_path}")
        except Exception as e:
            logging.error(f"Failed to save inverted image to {output_path}: {e}")

    @staticmethod
    def invert_png_file(path_file: str) -> None:
        """Inverts the colors of a PNG file and saves it to the output folder."""
        # Read image
        img_filename = os.path.basename(path_file)
        image = utils.image_handler.get_img_file(config.INPUT_FOLDER, img_filename)
        if not image:
            logging.error(f"Could not read image {img_filename}")
            return
        
        # Invert colors
        image = image.convert("RGB")
        inverted_image = ColorInverter.invert_image(image)

        # Save inverted image
        ImageInverter.save_inverted_image(inverted_image, os.path.join(config.OUTPUT_FOLDER, f"inverted_{img_filename}"))

class PDFInverter:
    """Handles PDF inversion logic."""

    @staticmethod
    def invert_pdf(path_file: str) -> None:
        """Inverts the colors of each page in a PDF file and saves it to the output folder."""
        # Get pdf file
        pdf_filename = os.path.basename(path_file)
        pdf_document = utils.pdf_handler.get_pdf_file(config.INPUT_FOLDER, pdf_filename)
        if not pdf_document:
            return
        
        # Transform pdf pages to images
        images = [page.get_pixmap() for page in pdf_document]
        if not images:
            return
        
        # Invert color of each page image
        inverted_images = []
        for img in images:
            pil_image = Image.frombytes("RGB", [img.width, img.height], img.samples)
            inverted_image = ColorInverter.invert_image(pil_image)
            inverted_images.append(inverted_image)

        # Merge the images in one file
        pdf_output_path = os.path.join(config.OUTPUT_FOLDER, f"inverted_{pdf_filename}")
        utils.image_handler.merge_images_in_one_pdf(inverted_images, pdf_output_path)
        
    @staticmethod
    def invert_pdfs_in_folder(input_folder: str) -> None:
        """Inverts all PDF files in the specified input folder."""
        pdf_files = utils.pdf_handler.get_pdf_files(input_folder)
        for pdf_path in pdf_files:
            PDFInverter.invert_pdf(pdf_path)
        
        logging.info(f"Completed inversion of all PDFs in folder {input_folder}")
