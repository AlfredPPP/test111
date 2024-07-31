# src/HiTrustHandler/pdf_handler/pdf_processor.py
import pdfplumber

def process_pdf(file_path):
    with pdfplumber.open(file_path) as pdf:
        first_page = pdf.pages[0]
        text = first_page.extract_text()
        # Process the PDF text and determine the TYPE
        return text
