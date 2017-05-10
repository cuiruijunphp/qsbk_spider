# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from localtest.settings import USER_AGENT_LIST
import random
from scrapy import signals
from scrapy import log
from scrapy.conf import settings
import base64


class LocaltestSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


#随机头
class RandomUserAgentMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def process_request(self,request, spider):
        # user_agent_list = settings.get('USER_AGENT_LIST')
        # ua = random.choice(user_agent_list)
        #文件路径写到这里
        user_agent_path = 'localtest/common/useragents.txt'
        with open(user_agent_path) as f:
            USER_AGENT_LIST = [line.strip() for line in f.readlines()]
            ua = random.choice(USER_AGENT_LIST)
            if ua :
                request.headers.setdefault('User-Agent',ua)
                print(ua)

#代理ip
class MyProxyMiddleware(object):
    # 代理服务器
    proxyServer = "http://proxy.abuyun.com:9020"

    # 代理隧道验证信息
    proxyUser = "用户名"
    proxyPass = "密码"

    proxyAuth = "Basic " + base64.urlsafe_b64encode(bytes((proxyUser + ":" + proxyPass), "ascii")).decode("utf8")

    def process_request(self, request, spider):
        print('>>>>>> proxyAuth:' + self.proxyAuth)
        request.meta['proxy'] = self.proxyServer
        request.headers['Proxy-Authorization'] = self.proxyAuth
        # request.headers.setdefault('Proxy-Authorization', self.proxyAuth)
        print('--------')


