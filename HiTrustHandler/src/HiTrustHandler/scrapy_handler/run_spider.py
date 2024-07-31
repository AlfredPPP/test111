# src/HiTrustHandler/scrapy_handler/run_spider.py
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from .spiders.login_spider import LoginSpider

def run_spider(username, password):
    configure_logging()
    runner = CrawlerRunner()
    deferred = runner.crawl(LoginSpider, username=username, password=password)
    deferred.addBoth(lambda _: reactor.stop())
    reactor.run()
