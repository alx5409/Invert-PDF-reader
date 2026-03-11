import fitz
import logging
from PIL import Image
import os

from configuration import config
import utils


class ColorInverter:
    """Handles color inversion logic."""

    def invert_single_color(color: int) -> int:
        """Inverts a color value based on the maximum color number defined in config."""
        return config.COLOR_NUMBER - color

    def invert_image(image: Image.Image) -> Image.Image:
        """Inverts the colors of a PIL Image and returns the inverted image."""
        return Image.eval(image, lambda x: ColorInverter.invert_single_color(x))


class ImageInverter:
    """Handles image inversion logic."""

    def save_inverted_image(image: Image.Image, output_path: str) -> None:
        """Saves the inverted image to the specified output path."""
        try:
            image.save(output_path)
            logging.info(f"Inverted image saved to {output_path}")
        except Exception as e:
            logging.error(f"Failed to save inverted image to {output_path}: {e}")

    def invert_png_file(path_file: str) -> None:
        """Inverts the colors of a PNG file and saves it to the output folder."""
        img_filename = os.path.basename(path_file)
        image = utils.image_handler.get_img_file(config.INPUT_FOLDER, img_filename)
        if not image:
            logging.error(f"Could not read image {img_filename}")
            return

        image = image.convert("RGB")
        inverted_image = ColorInverter.invert_image(image)
        output_path = os.path.join(config.OUTPUT_FOLDER, f"inverted_{img_filename}")
        ImageInverter.save_inverted_image(inverted_image, output_path)


class PDFInverter:
    """Handles PDF color transform logic without rasterizing pages."""

    def invert_pdf(path_file: str) -> None:
        """Recolor PDF pages without converting pages to images."""
        pdf_filename = os.path.basename(path_file)
        source_document = utils.pdf_handler.get_pdf_file(config.INPUT_FOLDER, pdf_filename)
        if not source_document:
            return

        output_document = fitz.open()
        try:
            for page in source_document:
                output_page = output_document.new_page(width=page.rect.width, height=page.rect.height)
                output_page.show_pdf_page(output_page.rect, source_document, page.number)
                # Recolor text, images, and vector graphics to grayscale.
                output_page.recolor(components=1)

            pdf_output_path = os.path.join(config.OUTPUT_FOLDER, f"inverted_{pdf_filename}")
            output_document.save(pdf_output_path, garbage=4, deflate=True, clean=True)
            logging.info(f"Recolored PDF saved to {pdf_output_path}")
        except Exception as e:
            logging.error(f"Failed to recolor PDF {pdf_filename}: {e}")
        finally:
            output_document.close()
            source_document.close()

    def invert_pdfs_in_folder(input_folder: str) -> None:
        """Recolors all PDFs in the specified input folder."""
        pdf_files = utils.pdf_handler.get_pdf_files(input_folder)
        for pdf_path in pdf_files:
            PDFInverter.invert_pdf(pdf_path)

        logging.info(f"Completed recolor of all PDFs in folder {input_folder}")


def invert_png_file(path_file: str) -> None:
    """Wrapper function to invert a PNG file."""
    ImageInverter.invert_png_file(path_file)


def invert_pdf(path_file: str) -> None:
    """Wrapper function to recolor a PDF file."""
    PDFInverter.invert_pdf(path_file)


def invert_pdfs_in_folder(input_folder: str) -> None:
    """Wrapper function to recolor all PDFs in a folder."""
    PDFInverter.invert_pdfs_in_folder(input_folder)
