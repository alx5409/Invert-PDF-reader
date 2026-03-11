# Invert-PDF-reader

Inverts the colors of PDF files and images (black to white and viceversa) to enable dark mode reading.

## How it works

- **PDF files**: injects a PDF `Difference` blend-mode overlay directly into each page content stream — no rasterization, so text stays sharp and file size stays small.
- **Image files** (PNG, JPG, BMP, GIF): performs a per-pixel color inversion using Pillow.

## Usage

1. Place your PDF or image file in the `input/` folder. Set this input folder path in the `.env`.
2. Run the script: `python main.py`.
3. The inverted file will be saved in the `output/` folder with the same name but with `_inverted` appended before the file extension.