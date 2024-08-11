# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import base64

import requests
from scrapy import signals
import random
from wangyi.settings import USER_AGENT_LIST
from wangyi.settings import PROXY_LIST
from selenium import webdriver
import time
from scrapy.http import HtmlResponse

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


# class WangyiSpiderMiddleware:
#     # Not all methods need to be defined. If a method is not defined,
#     # scrapy acts as if the spider middleware does not modify the
#     # passed objects.
#
#     @classmethod
#     def from_crawler(cls, crawler):
#         # This method is used by Scrapy to create your spiders.
#         s = cls()
#         crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
#         return s
#
#     def process_spider_input(self, response, spider):
#         # Called for each response that goes through the spider
#         # middleware and into the spider.
#
#         # Should return None or raise an exception.
#         return None
#
#     def process_spider_output(self, response, result, spider):
#         # Called with the results returned from the Spider, after
#         # it has processed the response.
#
#         # Must return an iterable of Request, or item objects.
#         for i in result:
#             yield i
#
#     def process_spider_exception(self, response, exception, spider):
#         # Called when a spider or process_spider_input() method
#         # (from other spider middleware) raises an exception.
#
#         # Should return either None or an iterable of Request or item objects.
#         pass
#
#     def process_start_requests(self, start_requests, spider):
#         # Called with the start requests of the spider, and works
#         # similarly to the process_spider_output() method, except
#         # that it doesn’t have a response associated.
#
#         # Must return only requests (not items).
#         for r in start_requests:
#             yield r
#
#     def spider_opened(self, spider):
#         spider.logger.info("Spider opened: %s" % spider.name)
#
#
# class WangyiDownloaderMiddleware:
#     # Not all methods need to be defined. If a method is not defined,
#     # scrapy acts as if the downloader middleware does not modify the
#     # passed objects.
#
#     @classmethod
#     def from_crawler(cls, crawler):
#         # This method is used by Scrapy to create your spiders.
#         s = cls()
#         crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
#         return s
#
#     def process_request(self, request, spider):
#         # Called for each request that goes through the downloader
#         # middleware.
#
#         # Must either:
#         # - return None: continue processing this request
#         # - or return a Response object
#         # - or return a Request object
#         # - or raise IgnoreRequest: process_exception() methods of
#         #   installed downloader middleware will be called
#         return None
#
#     def process_response(self, request, response, spider):
#         # Called with the response returned from the downloader.
#
#         # Must either;
#         # - return a Response object
#         # - return a Request object
#         # - or raise IgnoreRequest
#         return response
#
#     def process_exception(self, request, exception, spider):
#         # Called when a download handler or a process_request()
#         # (from other downloader middleware) raises an exception.
#
#         # Must either:
#         # - return None: continue processing this exception
#         # - return a Response object: stops process_exception() chain
#         # - return a Request object: stops process_exception() chain
#         pass
#
#     def spider_opened(self, spider):
#         spider.logger.info("Spider opened: %s" % spider.name)

'''
设置随机请求 user agent
'''
class RandomUserAgent(object):
    def process_request(self, reqeust, spider):
        ua = random.choice(USER_AGENT_LIST)
        reqeust.headers['User-Agent'] = ua

'''
设置随机请求代理 IP
'''
class RandomProxy(object):
    proxy = random.choice(PROXY_LIST)

    if 'user_passwd' in proxy:
        # 对账号密码进行加密，进行设置认证
        b64_up = base64.b64encode(proxy['user_passwd'].encode('utf-8'))
        # Basic 后面空格不能少
        requests.headers['Proxy-Authorization'] = 'Basic ' + b64_up.decode('utf-8')
        requests.meta['proxy'] = proxy['ip_port']
    else:
        requests.meta['proxy'] = proxy['ip_port']

'''
设置使用 selenuim 动态加载
'''
class SeleniumMiddleware(object):
    def process_request(self, request, spider):
        url = request.url

        # 设置过滤渲染条件
        if 'daydata' in url:
            driver = webdriver.Chrome()
            driver.get(url)
            time.sleep(3)

            # 获取渲染后的源码
            data = driver.page_source

            driver.close()

            # 创建响应对象
            res = HtmlResponse(url=url, body=data, encoding='utf-8', request=request)

            return res