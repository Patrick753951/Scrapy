import scrapy


class Job2Spider(scrapy.Spider):
    name = "job2"
    allowed_domains = ["163.com"]
    start_urls = ["https://163.com"]

    def parse(self, response):
        pass
