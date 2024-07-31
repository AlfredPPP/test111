# HiTrust Handler

HiTrust Handler is a Python-based project designed to handle login, PDF processing, and data posting tasks using Flask, Vue.js, pdfplumber, and Scrapy. This project follows the structure of the Python Project Template.

## Project Structure
```
HiTrustHandler/
├── .devcontainer/
│ ├── devcontainer.json
│ └── Dockerfile
├── .github/
│ ├── ISSUE_TEMPLATE/
│ │ ├── bug_report.md
│ │ └── feature_request.md
│ ├── workflows/
│ │ ├── build.yml
│ │ └── tests.yml
├── .vscode/
│ ├── launch.json
│ └── settings.json
├── docs/
│ ├── index.md
│ └── usage.md
├── src/
│ ├── HiTrustHandler/
│ │ ├── init.py
│ │ ├── app/
│ │ │ ├── init.py
│ │ │ ├── main.py
│ │ │ ├── templates/
│ │ │ │ └── index.html
│ │ │ ├── static/
│ │ │ │ ├── css/
│ │ │ │ │ └── styles.css
│ │ │ │ └── js/
│ │ │ │ └── app.js
│ │ ├── pdf_handler/
│ │ │ ├── init.py
│ │ │ └── pdf_processor.py
│ │ ├── scrapy_handler/
│ │ │ ├── init.py
│ │ │ ├── spiders/
│ │ │ │ ├── init.py
│ │ │ │ └── login_spider.py
│ │ │ ├── items.py
│ │ │ ├── middlewares.py
│ │ │ ├── pipelines.py
│ │ │ └── settings.py
│ │ ├── utils/
│ │ │ ├── init.py
│ │ │ └── helpers.py
│ │ └── config.py
├── tests/
│ ├── init.py
│ ├── test_app.py
│ ├── test_pdf_processor.py
│ ├── test_scrapy_handler.py
│ └── test_helpers.py
├── .gitignore
├── README.md
├── requirements.txt
└── setup.py
```
## Getting Started

### Prerequisites

- Python 3.8 or higher
- Node.js and npm (for Vue.js)
- Docker (optional, for development container)

### Installation

1. Clone the repository:
```
git clone https://github.com/yourusername/HiTrustHandler.git
cd HiTrustHandler
```
2. Create a virtual environment and activate it:
```
python -m venv venv
source venv/bin/activate # On Windows use `venv\Scripts\activate`
```
3. Install the required Python packages:
```
pip install -r requirements.txt
```

4. Navigate to the `src/HiTrustHandler/app` directory and install the required Node packages:

```
cd src/HiTrustHandler/app
npm install
```

### Running the Application

1. Start the Flask application:

```
python src/HiTrustHandler/app/main.py
```

2. Open a web browser and go to `http://localhost:5000` to access the UI.

### Running Tests

To run the tests, use the following command:

```
pytest tests/
```

## Usage

1. **Login**: Enter your account and password to log in to the specified site.
2. **Input Source**: After a successful login, input the remote file address.
3. **Process PDF**: The application will process the PDF file from the provided address.
4. **Post Data**: The processed data will be posted to the specified website, and a success message will be displayed upon completion.

## Contributing

Contributions are welcome! Please fork the repository and create a pull request.

## License

This project is licensed under the MIT License.

## Acknowledgements

- Flask
- Vue.js
- pdfplumber
- Scrapy

