# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

def dbHander():
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='gaia_poi', charset='utf8')
    return conn


class QsbkPipeline(object):

    def process_item(self, item, spider):
        conn = dbHander()
        cursor = conn.cursor()

        try:
            sql = "INSERT INTO qb_content(url,content) VALUES(%s,%s) "
            content = item['content']
            url = item['url']
            cursor.execute(sql,(url,content))
            conn.commit()
        except Exception:
            pass

        return item

    def __close__(self):
        self.conn.close()