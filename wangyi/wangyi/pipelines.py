# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import csv
import os
from datetime import time
from pymongo import MongoClient

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class WangyiPipeline:
    def open_spider(self, spider):
        if spider.name == 'job':
            # 创建时间戳
            timestamp = time.strftime("%Y%m%d%H%M%S")

            # 定义文件路径并拼接文件名
            self.file_path = os.path.join('./ScrapyDemo/outputs', 'job_' + timestamp + '.csv')

            # 当爬虫开始运行时，打开CSV文件进行写入
            self.file = open(self.file_path, 'a', newline='', encoding='utf-8')
            self.writer = csv.writer(self.file)
            self.writer.writerow(['Name', 'title', 'desc'])  # 写入标题头
        else:
            pass
    def process_item(self, item, spider):
        if spider.name == 'job':
            # 创建时间戳
            timestamp = time.strftime("%Y%m%d%H%M%S")

            # 定义文件路径并拼接文件名
            self.file_path = os.path.join('./ScrapyDemo/outputs', 'teachers_' + timestamp + '.csv')

            # 当爬虫开始运行时，打开CSV文件进行写入
            self.file = open(self.file_path, 'a', newline='', encoding='utf-8')
            self.writer = csv.writer(self.file)
            self.writer.writerow(['Name', 'title', 'desc'])  # 写入标题头
        else:
            pass

    def close_spider(self, spider):
        if spider.name == 'job':
            # 爬虫结束时关闭CSV文件
            self.file.close()
        else:
            pass

class WangyiSimplePipeline:
    def open_spider(self, spider):
        if spider.name == 'jobSimple':
            # 创建时间戳
            timestamp = time.strftime("%Y%m%d%H%M%S")

            # 定义文件路径并拼接文件名
            self.file_path = os.path.join('./ScrapyDemo/outputs', 'jobSSimple_' + timestamp + '.csv')

            # 当爬虫开始运行时，打开CSV文件进行写入
            self.file = open(self.file_path, 'a', newline='', encoding='utf-8')
            self.writer = csv.writer(self.file)
            self.writer.writerow(['Name', 'title', 'desc'])  # 写入标题头
        else:
            pass
    def process_item(self, item, spider):
        if spider.name == 'jobSimple':
            # 创建时间戳
            timestamp = time.strftime("%Y%m%d%H%M%S")

            # 定义文件路径并拼接文件名
            self.file_path = os.path.join('./ScrapyDemo/outputs', 'teachers_' + timestamp + '.csv')

            # 当爬虫开始运行时，打开CSV文件进行写入
            self.file = open(self.file_path, 'a', newline='', encoding='utf-8')
            self.writer = csv.writer(self.file)
            self.writer.writerow(['Name', 'title', 'desc'])  # 写入标题头
        else:
            pass

    def close_spider(self, spider):
        if spider.name == 'jobSimple':
            # 爬虫结束时关闭CSV文件
            self.file.close()
        else:
            pass

'''
写入 DB
'''
class MongoPipeline(object):
    def open_spider(self, spider):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client['wangyi']
        self.col = self.db['job']

    def process_item(self, item, spider):
        data = dict(item)
        self.col.insert(data)

        return item

    def close_spider(self, spider):
        self.client.close()