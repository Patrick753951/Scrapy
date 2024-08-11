# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WangyiItem(scrapy.Item):
    # define the fields for your item here like:
    # 职位名称
    name = scrapy.Field()

    # 全职、兼职、实习
    time = scrapy.Field()

    # 工作城市
    city = scrapy.Field()

    # 所属公司
    company = scrapy.Field()

    # 职位类别
    type = scrapy.Field()

    # 招聘人数
    position_number = scrapy.Field()

    # 学历要求
    edu = scrapy.Field()

    # 工作经验
    exp = scrapy.Field()

    # 更新时间
    updated = scrapy.Field()

class WangyiSimpleItem(scrapy.Item):
    # define the fields for your item here like:
    # 职位名称
    name = scrapy.Field()

    # 全职、兼职、实习
    time = scrapy.Field()

    # 工作城市
    city = scrapy.Field()

    # 所属公司
    company = scrapy.Field()

    # 职位类别
    type = scrapy.Field()

    # 招聘人数
    position_number = scrapy.Field()

    # 学历要求
    edu = scrapy.Field()

    # 工作经验
    exp = scrapy.Field()

    # 更新时间
    updated = scrapy.Field()
