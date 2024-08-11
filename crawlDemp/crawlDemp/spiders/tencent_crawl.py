import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class TencentCrawlSpider(CrawlSpider):
    name = "tencent_crawl"
    allowed_domains = ["tencent.com"]
    start_urls = ["https://tencent.com"]

    # 连接提取规则
    rules = (
        # 使用 Rule 类生成提取规则
        # LinkExtractor 用去设置连接提取规则，一般使用 allow 参数，接收正则表达式
        # follow 决定是否在连接提取器提取的连接的对应响应中，继续使用连接提取器提取连接

        # 设置详情页面连接提取规则
        Rule(LinkExtractor(allow=r"positiond_details.php\?id=\d+"), callback="parse_item"),
        # 设置翻页连接提取规则
        Rule(LinkExtractor(allow=r"position.php\?start=\d+"), follow=True),

    )

    def parse_item(self, response):
        item = {}
        #item["domain_id"] = response.xpath('//input[@id="sid"]/@value').get()
        #item["name"] = response.xpath('//div[@id="name"]').get()
        #item["description"] = response.xpath('//div[@id="description"]').get()
        yield item
