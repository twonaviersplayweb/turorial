# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from scrapy import signals
import json
import codecs

basedir = os.path.abspath(os.path.dirname(__file__))
sqlite_url = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')

engine = create_engine(sqlite_url, echo=True)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class TurorialPipeline(object):
    def __init__(self):
        self.file = codecs.open('book.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        return item

    def spider_closed(self, spider):
        self.file.close()

class Book(Base):
    __tablename__ = 'book'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    pic_url = Column(String)
    pub = Column(String)
    breif = Column(String)

    def __repr(self):
        return "<Book(name='%s', pic_url='%s', pub='%s', breif='%s')>" % (
            self.name, self.pic_url, self.pub, self.breif
        )


from scrapy import signals
import json
import codecs
class JsonWithEncodingCnblogsPipeline(object):
	def __init__(self):
		self.file = codecs.open('cnblogs.json', 'w', encoding='utf-8')
	def process_item(self, item, spider):
		line = json.dumps(dict(item), ensure_ascii=False) + "\n"
		self.file.write(line)
		return item
	def spider_closed(self, spider):
		self.file.close()