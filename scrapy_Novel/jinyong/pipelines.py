# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html



#mysql
import pymysql



# class JinyongPipeline(object):
#     def open_spider(self,spider):
#         """
#         建立数据库链接
#         """
#         self.conn = pymysql.connect(host='127.0.0.1',port=3306,user='root',
#                                     db='NewTable',password="cai1299851090",charset="utf8")
#         self.cursor = self.conn.cursor()
#
#     def process_item(self, item, spider):
#         sql = 'insert into book (book_name,dir_name,dir_content) VALUES (%s,%s,%s)'
#         self.cursor.execute(sql, (item['book_name'], item['dir_name'], item['dir_content']))
#         self.conn.commit()
#         return item
#
#     def close_spider(self,spider):
#         """
#         关闭数据库
#         :param spider:
#         :return:
#         """
#         self.cursor.close()
#         self.conn.close()
from twisted.enterprise import adbapi
from pymysql import cursors

class JinyongPipeline(object):
    def __init__(self, dbpool):
        # 初始化线程池对象，用于维护操作mysql写入操作的线程
        self.dbpool = dbpool
    # from_settings()函数是固定写法，该函数是用于读取settings.py配置信息的函数，第二个参数settings是一个字典。
    @classmethod
    def from_settings(cls, settings):
        args = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWORD'],
            charset=settings['MYSQL_CHARSET'],
            # 指定用用于创建cursor游标的类
            cursorclass=cursors.DictCursor,
        )
        # 创建一个线程池对象
        # 参数1：用于连接MySQL数据库的驱动
        # 参数2：数据库的链接信息（host, port, user等）
        dbpool = adbapi.ConnectionPool("pymysql", **args)
        return cls(dbpool)

    def process_item(self, item, spider):
        # 在线程池dbpool中通过调用runInteraction()函数，来实现异步插入数据的操作。runInteraction()会insert_sql交由线程池中的某一个线程执行具体的插入操作。
        query = self.dbpool.runInteraction(self.insert, item)
        # addErrorback()数据库异步写入失败时，会执行addErrorback()内部的函数调用。
        query.addErrback(self.handler_error)
        return item

    def handler_error(self, failure):
        print("插入数据库失败",failure)

    def insert(self, cursor, item):
        sql = 'insert into book (book_name,dir_name,dir_content) VALUES (%s,%s,%s)'
        cursor.execute(sql, (item['book_name'], item['dir_name'], item['dir_content']))
        # 不需要执行commit()的操作了，会在线程池中自动指定提交的操作。

