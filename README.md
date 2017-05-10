# qsbk_spider
抓取糗事百科纯文本段子

抓取的地址为：
http://www.qiushibaike.com/ 以及 http://www.qiushibaike.com/text/ 和 http://www.qiushibaike.com/textnew/ 这三个页面下的纯文本段子。

抓取语言: 
    
- python3 + scrpay + mysql 存储，数据库表名为qb_content

爬虫运行:
    
- cmd中 切换到相应目录，scrapy crawl qsbk

说明:

-     1.爬虫中已经使用了随机浏览器头(将浏览器头信息保存到了一个文件中)
-     2.使用ip代理，用了阿布云，使用高匿ip抓取成功，不被墙的几率要高好多
-     3.如果爬取结果状态码是[500, 503, 504, 400, 403, 404, 408]，则重试(retry下载中间件)
-     4.由于目前这几个地址总页码都是35，所以，代码里直接写死了，建议是解析出来页码信息，最好不要写死

ps：此爬虫是自己没事做着玩的，后面会继续完善
