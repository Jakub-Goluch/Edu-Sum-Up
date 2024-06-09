from fpdf import FPDF
from pdf2image import convert_from_path
import easyocr
import numpy as np


# pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe" # PATH to a tesseract exe

def delete_special_characters(word):
    for character in word:
        if ord(character) > 127:
            return False
    return True


# def convert_images_to_searchable_pdf(pdf_path: str, return_path: str) -> None:
#     """Extracts text from an image and saves it as pdf file to user device"""
#     images = convert_from_path(pdf_path, poppler_path="C:\\Program Files\\Poppler\\poppler-24.02.0\\Library\\bin") # PATH to a bin folder of Poppler
#     pdf = FPDF()
#     for i, image in enumerate(images):
#         text = pytesseract.image_to_string(image, lang="eng")
#         pdf.add_page()
#
#         pdf.set_font("Arial", size=15)
#
#         for line in text.split('\n'):
#             if delete_special_characters(line):
#                 pdf.cell(200, 10, txt=line, ln=1, align='C')
#
#     pdf.output(return_path)
#
#
# pdf1 = "C:\\Users\\Kuba\\Desktop\\Python\\Edu-Sum-Up\\examples\\artykul.pdf"
# pdf2 = "C:\\Users\\Kuba\\Desktop\\Python\\Edu-Sum-Up\\examples\\artykul_1.pdf"
#
# convert_images_to_searchable_pdf(pdf1, pdf2)

def convert_images_to_searchable_pdf(pdf_path: str, return_path: str) -> None:
    """Extracts text from an image and saves it as pdf file to user device"""
    reader = easyocr.Reader(['en', 'pl'])  # this needs to run only once to load the model into memory
    images = convert_from_path(pdf_path,
                               poppler_path="C:\\Program Files\\Poppler\\poppler-24.02.0\\Library\\bin")  # PATH to a bin folder of Poppler
    pdf = FPDF()
    for i, image in enumerate(images):
        image_array = np.array(image)
        print(image_array)
        result = reader.readtext(image_array, detail=0)
        text = ' '.join([res[1] for res in result])
        pdf.add_page()

        pdf.set_font("Arial", size=15)

        for line in result:
            if delete_special_characters(line):
                pdf.cell(200, 10, txt=line, ln=1, align='C')

    pdf.output(return_path)
