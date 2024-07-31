# src/HiTrustHandler/utils/helpers.py
import requests

def download_pdf(url):
    response = requests.get(url)
    file_path = 'path_to_save_pdf.pdf'
    with open(file_path, 'wb') as file:
        file.write(response.content)
    return file_path

def determine_type(pdf_text):
    # Implement logic to determine the TYPE based on PDF text
    if 'certain_keyword' in pdf_text:
        return 'TYPE_A'
    else:
        return 'TYPE_B'
