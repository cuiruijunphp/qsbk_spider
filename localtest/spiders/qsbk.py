# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from localtest.items import QiushibaikeItem


class QsbkSpider(scrapy.Spider):
    name = "qsbk"
    allowed_domains = ["qiushibaike.com"]
    # start_urls = ['http://www.qiushibaike.com/','http://www.qiushibaike.com/textnew/','http://www.qiushibaike.com/text/']
    par_url = "http://www.qiushibaike.com"

    custom_settings = {
        'DOWNLOAD_DELAY': 1,
        'ITEM_PIPELINES': {
            'localtest.pipelines.QsbkPipeline': 300,
        },
        'DOWNLOADER_MIDDLEWARES': {
            "scrapy.downloadermiddleware.useragent.UserAgentMiddleware": None,
            "localtest.middlewares.RandomUserAgentMiddleware": 200,
            'scrapy.downloadermiddlewares.retry.RetryMiddleware': 543,
            # "localtest.middlewares.MyProxyMiddleware": 250,
        }
    }

    def start_requests(self):
        for i in range(1,36):
            url_index = "http://www.qiushibaike.com/8hr/page/"+str(i)
            url_text = "http://www.qiushibaike.com/text/page/"+str(i)
            url_textnew = "http://www.qiushibaike.com/textnew/page/"+str(i)
            yield Request(url_index,callback=self.parse)
            yield Request(url_text,callback=self.parse)
            yield Request(url_textnew,callback=self.parse)

    def parse(self, response):
        for row in response.xpath('//a[@class="contentHerf"]'):
            itemss = QiushibaikeItem()
            #如果有图片的情况这条就直接舍弃
            #取图片xpath
            thumb_class = row.xpath('following-sibling::div[1]/@class').extract_first()
            # print(thumb_class)
            if thumb_class == 'thumb':
                continue

            url = row.xpath('@href').extract_first()
            itemss['url'] = self.par_url + url
            result = row.xpath('div[@class="content"]/span').extract()
            if len(result) == 1:
                content = result[0].lstrip('<span>').rstrip('</span>').strip()
                itemss['content'] = content
            #查看全文的情况
            if len(result) == 2:
                # content = result.extract().lstrip('<span>').rstrip('</span>')
                # itemss['content'] = content
                yield Request(self.par_url + url,callback=self.parse_all_text)

            yield itemss

    def parse_all_text(self,response):
        #查看全文
        itemss = QiushibaikeItem()
        content = response.xpath('//div[@id="single-next-link"]/div').extract_first()
        itemss['url'] = response.url
        itemss['content'] = content.lstrip('<div class="content">').rstrip('</div>').strip()

        yield itemss


