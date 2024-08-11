import scrapy
from wangyi.wangyi.items import WangyiItem


class PositionSpider(scrapy.Spider):
    name = "jobs"
    allowed_domains = ["163.com"]
    start_urls = ["https://hr.163.com/job-list.html"]

    def parse(self, response):
        # 提取数据
        node_list = response.xpath("//div[@class='content-base']")
        for num, node in enumerate(node_list):
            # 设置过滤条件
            if num % 2 == 0:
                item = WangyiItem()

                # 使用 strip 去除结尾多余空格
                item['name'] = node.xpath("./div[@class='content-base-left']/h3/a/text()").extract_first().strip()
                item['position_number'] = node.xpath("./div[@class='content-base-left']/h3/span/text()").extract_first()
                item['city'] = node.xpath("./div[@class='content-base-left']/p[1]/span[1]/text()").extract_first()
                item['type'] = node.xpath("./div[@class='content-base-left']/p[1]/span[2]/text()").extract_first()
                item['edu'] = node.xpath("./div[@class='content-base-left']/p[1]/span[3]/text()").extract_first()
                item['exp'] = node.xpath("./div[@class='content-base-left']/p[1]/span[4]/text()").extract_first()
                item['time'] = node.xpath("./div[@class='content-base-left']/p[1]/span[5]/text()").extract_first()
                item['link'] = response.urljoin(node.xpath("./div[@class='content-base-left']/h3/a/@href").extract_first())

                # yield item
                # 构建详情页请求
                yield scrapy.Request(
                    url=item['link'],
                    callback=self.parse_detail,
                    meta={'item': item}
                )

        # 模拟翻页
        part_url = response.xpath("//a[@class='next']/@href").extract_first()

        # 判断终止条件
        if part_url != 'javascript:void[0]':
            next_url = response.url.join(part_url)

            # 构建请求对象并返回给引擎
            yield scrapy.Request(
                url=next_url,
                # 执行对应 url 由谁来解析，也可以传给第二个 parse 方法解析（存在第二个页面解析方法不一样的情况）
                # callback 不写默认由 parse 解析
                # callback=self.parse_next_page
                callback=self.parse
            )

        # 第二个 parse 方法，用于解析下一页或其他特定URL的响应

    def parse_detail(self, response):
        # print(response.meta['item'])
        # 将 meta 传参获取数据
        item = response.meta['item']
        
        # 对剩余数据进行处理

        # 返回给引擎
        yield item