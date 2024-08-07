# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

'''
进行建模
提前定义采集哪些字段
可以防止手误，采集的时候会自动校验
'''

class ScrapydemoItem(scrapy.Item):
    # define the fields for your item here like:
    # 讲师姓名
    name = scrapy.Field()

    # 讲师头衔
    title = scrapy.Field()

    # 讲师简介
    desc = scrapy.Field()