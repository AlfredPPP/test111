# src/HiTrustHandler/app/main.py
from flask import Flask, render_template, request, jsonify
from .scrapy_handler.run_spider import run_spider
from .pdf_handler.pdf_processor import process_pdf
from .utils.helpers import download_pdf, determine_type

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    # Add login logic here, for now, we just return success
    return jsonify({'status': 'success'})

@app.route('/submit_source', methods=['POST'])
def submit_source():
    data = request.json
    source = data.get('source')
    # Add source processing logic here, for now, we just return success
    return jsonify({'status': 'success'})

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    # Run Scrapy spider for login
    run_spider(username, password)
    return jsonify({'status': 'success'})

@app.route('/submit_source', methods=['POST'])
def submit_source():
    data = request.json
    source = data.get('source')
    # Download the PDF from the source URL (you need to implement this part)
    file_path = download_pdf(source)
    pdf_text = process_pdf(file_path)
    # Determine the TYPE based on the processed PDF text
    pdf_type = determine_type(pdf_text)
    # Run Scrapy spider to post data based on the TYPE
    run_spider_post_data(pdf_type)
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(debug=True)
