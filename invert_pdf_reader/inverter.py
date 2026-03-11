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
    """Handles PDF color inversion by injecting a Difference blend overlay into each page content stream."""

    def _register_difference_extgstate(doc: fitz.Document, page_xref: int, gs_xref: int) -> None:
        """Register GSDiff in page resources, resolving indirect Resources safely."""
        resources_type, resources_value = doc.xref_get_key(page_xref, "Resources")

        if resources_type == "xref":
            resources_xref = int(resources_value.split()[0])
            doc.xref_set_key(resources_xref, "ExtGState/GSDiff", f"{gs_xref} 0 R")
            return

        if resources_type == "dict":
            doc.xref_set_key(page_xref, "Resources/ExtGState/GSDiff", f"{gs_xref} 0 R")
            return

        resources_xref = doc.get_new_xref()
        doc.update_object(resources_xref, "<<>>")
        doc.xref_set_key(page_xref, "Resources", f"{resources_xref} 0 R")
        doc.xref_set_key(resources_xref, "ExtGState/GSDiff", f"{gs_xref} 0 R")

    def _invert_page_colors(doc: fitz.Document, page: fitz.Page) -> None:
        """Append a white Difference-blend rectangle as a separate content stream."""
        w = page.rect.width
        h = page.rect.height
        page_xref = page.xref

        # Register ExtGState with BM=Difference in page Resources.
        gs_xref = doc.get_new_xref()
        doc.update_object(gs_xref, "<</Type /ExtGState /BM /Difference>>")
        PDFInverter._register_difference_extgstate(doc, page_xref, gs_xref)

        # Difference+white overlay drawn LAST to invert all visible colors.
        invert_ops = (f"q /GSDiff gs 1 1 1 rg 0 0 {w:.4f} {h:.4f} re f Q\n").encode()
        overlay_xref = doc.get_new_xref()
        doc.update_object(overlay_xref, "<</Length 0>>")
        doc.update_stream(overlay_xref, invert_ops)

        existing = page.get_contents()
        refs = " ".join(f"{x} 0 R" for x in existing + [overlay_xref])
        doc.xref_set_key(page_xref, "Contents", f"[{refs}]")

    def invert_pdf(path_file: str) -> None:
        """Invert PDF page colors without rasterizing."""
        pdf_filename = os.path.basename(path_file)
        source_doc = utils.pdf_handler.get_pdf_file(config.INPUT_FOLDER, pdf_filename)
        if not source_doc:
            return

        output_doc = fitz.open()
        try:
            # Flatten annotations/widgets once so they are part of normal content.
            source_doc.bake()

            for source_page in source_doc:
                output_page = output_doc.new_page(
                    width=source_page.rect.width,
                    height=source_page.rect.height,
                )
                # Paint a stable white base in the output page before copying content.
                output_page.draw_rect(output_page.rect, fill=(1, 1, 1), color=None, overlay=False)
                output_page.show_pdf_page(output_page.rect, source_doc, source_page.number)
                PDFInverter._invert_page_colors(output_doc, output_page)

            pdf_output_path = os.path.join(config.OUTPUT_FOLDER, f"inverted_{pdf_filename}")
            output_doc.save(pdf_output_path, garbage=4, deflate=True, clean=True)
            logging.info(f"Inverted PDF saved to {pdf_output_path}")
        except Exception as e:
            logging.error(f"Failed to invert PDF {pdf_filename}: {e}")
        finally:
            output_doc.close()
            source_doc.close()

    def invert_pdfs_in_folder(input_folder: str) -> None:
        """Inverts all PDFs in the specified input folder."""
        pdf_files = utils.pdf_handler.get_pdf_files(input_folder)
        for pdf_path in pdf_files:
            PDFInverter.invert_pdf(pdf_path)

        logging.info(f"Completed inversion of all PDFs in folder {input_folder}")


def invert_png_file(path_file: str) -> None:
    """Wrapper function to invert a PNG file."""
    ImageInverter.invert_png_file(path_file)


def invert_pdf(path_file: str) -> None:
    """Wrapper function to recolor a PDF file."""
    PDFInverter.invert_pdf(path_file)


def invert_pdfs_in_folder(input_folder: str) -> None:
    """Wrapper function to recolor all PDFs in a folder."""
    PDFInverter.invert_pdfs_in_folder(input_folder)
