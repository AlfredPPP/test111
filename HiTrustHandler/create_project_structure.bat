@echo off
setlocal

rem Root directory
set ROOT_DIR=HiTrustHandler

rem Create root directory
mkdir %ROOT_DIR%

rem Create subdirectories
mkdir %ROOT_DIR%\.devcontainer
mkdir %ROOT_DIR%\.github\ISSUE_TEMPLATE
mkdir %ROOT_DIR%\.github\workflows
mkdir %ROOT_DIR%\.vscode
mkdir %ROOT_DIR%\docs
mkdir %ROOT_DIR%\src\HiTrustHandler\app\templates
mkdir %ROOT_DIR%\src\HiTrustHandler\app\static\css
mkdir %ROOT_DIR%\src\HiTrustHandler\app\static\js
mkdir %ROOT_DIR%\src\HiTrustHandler\pdf_handler
mkdir %ROOT_DIR%\src\HiTrustHandler\utils
mkdir %ROOT_DIR%\tests

rem Create files
rem Root files
type nul > %ROOT_DIR%\.gitignore
type nul > %ROOT_DIR%\README.md
type nul > %ROOT_DIR%\requirements.txt
type nul > %ROOT_DIR%\setup.py

rem .devcontainer files
type nul > %ROOT_DIR%\.devcontainer\devcontainer.json
type nul > %ROOT_DIR%\.devcontainer\Dockerfile

rem .github files
type nul > %ROOT_DIR%\.github\ISSUE_TEMPLATE\bug_report.md
type nul > %ROOT_DIR%\.github\ISSUE_TEMPLATE\feature_request.md
type nul > %ROOT_DIR%\.github\workflows\build.yml
type nul > %ROOT_DIR%\.github\workflows\tests.yml

rem .vscode files
type nul > %ROOT_DIR%\.vscode\launch.json
type nul > %ROOT_DIR%\.vscode\settings.json

rem docs files
type nul > %ROOT_DIR%\docs\index.md
type nul > %ROOT_DIR%\docs\usage.md

rem src files
type nul > %ROOT_DIR%\src\HiTrustHandler\__init__.py
type nul > %ROOT_DIR%\src\HiTrustHandler\app\__init__.py
type nul > %ROOT_DIR%\src\HiTrustHandler\app\main.py
type nul > %ROOT_DIR%\src\HiTrustHandler\app\templates\index.html
type nul > %ROOT_DIR%\src\HiTrustHandler\app\static\css\styles.css
type nul > %ROOT_DIR%\src\HiTrustHandler\app\static\js\app.js
type nul > %ROOT_DIR%\src\HiTrustHandler\pdf_handler\__init__.py
type nul > %ROOT_DIR%\src\HiTrustHandler\pdf_handler\pdf_processor.py
type nul > %ROOT_DIR%\src\HiTrustHandler\utils\__init__.py
type nul > %ROOT_DIR%\src\HiTrustHandler\utils\helpers.py
type nul > %ROOT_DIR%\src\HiTrustHandler\config.py

rem tests files
type nul > %ROOT_DIR%\tests\__init__.py
type nul > %ROOT_DIR%\tests\test_app.py
type nul > %ROOT_DIR%\tests\test_pdf_processor.py
type nul > %ROOT_DIR%\tests\test_scrapy_handler.py
type nul > %ROOT_DIR%\tests\test_helpers.py

rem Initialize Scrapy project
cd %ROOT_DIR%\src\HiTrustHandler
scrapy startproject scrapy_handler

rem Remove unnecessary files created by scrapy startproject command
del scrapy_handler\items.py
del scrapy_handler\pipelines.py
del scrapy_handler\settings.py

rem Create additional scrapy files
type nul > scrapy_handler\spiders\login_spider.py

echo Project structure created successfully.

endlocal
