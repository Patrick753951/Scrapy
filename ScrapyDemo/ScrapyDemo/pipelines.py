# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import csv
import json
import os
import time
from pathlib import Path

import pandas as pd
from scrapy import item
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class ScrapydemoPipeline:

    def open_spider(self, spider):
        # 创建时间戳
        timestamp = time.strftime("%Y%m%d%H%M%S")

        # 定义文件路径并拼接文件名
        self.file_path = os.path.join('./ScrapyDemo/outputs', 'teachers_' + timestamp + '.csv')

        # 当爬虫开始运行时，打开CSV文件进行写入
        self.file = open(self.file_path, 'a', newline='', encoding='utf-8')
        self.writer = csv.writer(self.file)
        self.writer.writerow(['Name', 'title', 'desc'])  # 写入标题头

    def process_item(self, item, spider):
        # 处理每个Item，将数据写入CSV文件
        self.writer.writerow([item['name'], item['title'], item['desc']])
        return item

    def close_spider(self, spider):
        # 爬虫结束时关闭CSV文件
        self.file.close()