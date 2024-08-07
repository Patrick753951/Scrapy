import scrapy

'''
爬虫流程
1. 修改起始 URL
2. 检查域名
3. 在 parse 方法中实现爬取逻辑
'''

class ItcastSpider(scrapy.Spider):
    name = "itcast"
    allowed_domains = ["itcast.cn"]
    # 设置起始 URL，只需要设置一个起始 URL，scrapy 会自动解析响应的链接，并访问这些链接
    start_urls = ["https://www.itheima.com/teacher.html"]

    # 解析响应，对于起始 URL 进行解析
    def parse(self, response):
        # 定义对于响应网站的相关操作
        # with open("../outputs/itcast.html", "wb") as f:
        #     f.write(response.body)

        # 获取所有教师节点
        node_list = response.xpath("//div[@class='li_txt']")
        # print(len(node_list))

        for node in node_list:
            temp = {}

            # xpath 方法返回的是选择器对象列表
            # xpath 只含有一个值的列表，使用 extract_first() 方法获取
            # xpath 含有多个值，使用 extract() 方法获取
            temp['name'] = node.xpath("./h3/text()").extract_first()
            temp['title'] = node.xpath("./h4/text()")[0].extract()
            temp['desc'] = node.xpath("./p/text()").extract_first()

            yield temp