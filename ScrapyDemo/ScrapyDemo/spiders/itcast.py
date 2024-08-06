import scrapy


class ItcastSpider(scrapy.Spider):
    name = "itcast"
    allowed_domains = ["itcast.cn"]
    # 设置起始 URL，只需要设置一个起始 URL，scrapy 会自动解析响应的链接，并访问这些链接
    start_urls = ["https://itcast.cn"]

    # 解析响应，对于起始 URL 进行解析
    def parse(self, response):
        # 定义对于响应网站的相关操作
        with open("itcast.html", "wb") as f:
            f.write(response.body)
