import os
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests


class ASXCrawler:
    """
    ASXCrawler is a web scraper designed to access and download specific announcement files
    from the ASX website based on the provided search key, title key, and year.

    Usage:
    1. Initialize the crawler with search_key, title_key, and year.
       search_key: The ASX code to search for (max length 3).
       title_key: The keywords to search for in the announcement titles (list of strings).
       year: The year to search within.

    2. Call the run() method to execute the crawler.
       The crawler will:
       - Visit the initial URL to obtain cookies.
       - Access the announcements page using the search key and year.
       - Extract announcement titles and check for the title keys.
       - Download the first matching file to the 'downloaded_pdf_files' directory.

    3. The downloaded files will be named in the format title_dd-mm-yyyy.pdf.

    Example:
    crawler = ASXCrawler(search_key='AIZ', title_keys=['Dividend', 'Distribution'], year='2024')
    crawler.run()
    """

    def __init__(self, search_key: str, title_keys: list, year: str, proxy: str = None):
        self.search_key = search_key
        self.title_keys = title_keys
        self.year = year
        self.base_url = 'https://www.asx.com.au'
        self.initial_url = 'https://www.asx.com.au/markets/trade-our-cash-market/historical-announcements'
        self.announcements_url = f'{self.base_url}/asx/v2/statistics/announcements.do?by=asxCode&asxCode={search_key}&timeframe=Y&year={year}'
        self.download_dir = 'downloaded_pdf_files'

        # Set up Chrome options for headless mode
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-extensions")

        # Set up proxy
        if proxy:
            chrome_options.add_argument(f'--proxy-server={proxy}')

        # Initialize WebDriver
        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, 10)

        # Set up logging
        logging.basicConfig(filename='crawler.log', level=logging.INFO, format='%(asctime)s %(message)s')
        self.logger = logging.getLogger()

    def get_initial_cookies(self):
        """Get initial cookies by visiting the initial URL."""
        self.driver.get(self.initial_url)
        # Wait for cookies to be set
        ready_state_script = "return document.readyState"
        while True:
            ready_state = self.driver.execute_script(ready_state_script)
            if ready_state == "complete":
                break

    def get_cookies_dict(self):
        """Retrieve cookies from the current session and format them for requests."""
        cookies = self.driver.get_cookies()
        cookies_dict = {cookie['name']: cookie['value'] for cookie in cookies}
        return cookies_dict

    def search_announcements(self):
        """Search announcements and filter results based on title_keys."""
        self.driver.get(self.announcements_url)
        try:
            self.wait.until(EC.presence_of_all_elements_located((By.XPATH, "//announcement_data//tbody/tr")))
            rows = self.driver.find_elements(By.XPATH, "//announcement_data//tbody/tr")
            for row in rows:
                date = row.find_element(By.XPATH, "./td[1]").text.split()[0]
                link = row.find_element(By.XPATH, "./td[3]//a")
                title = link.text
                for title_key in self.title_keys:
                    if title_key in title:
                        file_url = link.get_attribute("href")
                        return {
                            'title': title.split('\n')[0].replace('/', '-'),
                            'file_url': file_url,
                            'date': date.replace('/', '-')
                        }
        except Exception as e:
            self.logger.error(f"Error in search_announcements: {e}")
        return None

    def get_final_pdf_url(self, file_url):
        """Extract the hidden PDF URL without clicking the agree button."""
        self.driver.get(file_url)
        try:
            self.wait.until(EC.presence_of_element_located((By.NAME, "pdfURL")))
            pdf_url = self.driver.find_element(By.NAME, "pdfURL").get_attribute("value")
            self.logger.info("Extracted PDF URL.")
            return pdf_url
        except Exception as e:
            self.logger.error(f"Error in get_final_pdf_url: {e}")
            return None

    def download_file(self, pdf_url, title, date):
        """Download the file from the given URL."""
        try:
            response = requests.get(pdf_url, allow_redirects=True)
            if response.status_code == 200:
                if not os.path.exists(self.download_dir):
                    os.makedirs(self.download_dir)
                file_name = f'{self.download_dir}/{title}_{date}.pdf'
                with open(file_name, 'wb') as file:
                    file.write(response.content)
                self.logger.info(f"File downloaded: {file_name}")
            else:
                self.logger.error(f"Failed to download file, status code: {response.status_code}")
        except requests.RequestException as e:
            self.logger.error(f"Error in download_file: {e}")

    def run(self):
        """Run the crawler."""
        try:
            self.get_initial_cookies()
            # cookies = self.get_cookies_dict()
            result = self.search_announcements()
            if result:
                pdf_url = self.get_final_pdf_url(result['file_url'])
                if pdf_url:
                    self.download_file(pdf_url, result['title'], result['date'])
        except Exception as e:
            self.logger.error(f"Error in run: {e}")
        finally:
            self.driver.quit()


if __name__ == '__main__':
    # Example usage
    proxy = 'http://127.0.0.1:7890'  # Set up proxy if needed
    crawler = ASXCrawler(search_key='AIZ', title_keys=['Dividend', 'Distribution'], year='2024', proxy=proxy)
    crawler.run()
