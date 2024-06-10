from fpdf import FPDF
from pdf2image import convert_from_path
import easyocr
import numpy as np
import platform

# pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe" # PATH to a tesseract exe

def delete_special_characters(word):
    for character in word:
        if ord(character) > 127:
            return False
    return True


def convert_images_to_searchable_pdf(pdf_path: str, return_path: str) -> None:
    """Extracts text from an image and saves it as pdf file to user device"""
    reader = easyocr.Reader(['en'])
    if platform.system() == "Windows":
        images = convert_from_path(pdf_path, poppler_path="C:\\Program Files\\Poppler\\poppler-24.02.0\\Library\\bin")
    else:
        images = convert_from_path(pdf_path)
    pdf = FPDF()
    for i, image in enumerate(images):
        image_array = np.array(image)
        result = reader.readtext(image_array, detail=0)
        text = ' '.join([res[1] for res in result])
        pdf.add_page()

        pdf.set_font("Arial", size=15)

        for line in result:
            if delete_special_characters(line):
                pdf.cell(200, 10, txt=line, ln=1, align='C')

    pdf.output(return_path)
