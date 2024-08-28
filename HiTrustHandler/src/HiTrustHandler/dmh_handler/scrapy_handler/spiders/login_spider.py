# src/HiTrustHandler/dmh_handler/spiders/login_spider.py
import scrapy

class LoginSpider(scrapy.Spider):
    name = 'login_spider'
    start_urls = ['http://example.com/login']

    def __init__(self, username, password, *args, **kwargs):
        super(LoginSpider, self).__init__(*args, **kwargs)
        self.username = username
        self.password = password

    def parse(self, response):
        return scrapy.FormRequest.from_response(
            response,
            formdata={'username': self.username, 'password': self.password},
            callback=self.after_login
        )

    def after_login(self, response):
        if "authentication failed" in response.body.decode():
            self.logger.error("Login failed")
            return
        self.logger.info("Login succeeded")
        # Continue with your scraping logic here
