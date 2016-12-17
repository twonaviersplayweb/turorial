# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
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
tag_list = ['编程', '互联网', '旅行']

'''
# json
class TurorialPipeline(object):
    def __init__(self):
        self.file = codecs.open('book.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        return item

    def spider_closed(self, spider):
        self.file.close()
'''

# sqlite
class TurorialPipeline(object):
    def __init__(self):
        Base.metadata.create_all(engine)
        self.session = session
        Tag.books = relationship("Book", order_by=Book.id, back_populates='tag')

        for book_tag in tag_list:
            tag1 = Tag(name=book_tag)
            session.add(tag1)
            session.commit()


    def process_item(self, item, spider):
        # book = Book(name=item['name'], img_url=item['img_url'], pub=item['pub'],
        #             des=item['description'], tag=Tag(name=item['tag']))
        book = Book(name=item['name'], img_url=item['img_url'], pub=item['pub'],
                    des=item['description'])
        tag1 = self.session.query(Tag).filter_by(name=item['tag']).first()
        if tag1:
            book.tag = tag1
        self.session.add(book)
        self.session.commit()
        return item

    def spider_closed(self, spider):
        self.session.close()


class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    des = Column(String)
    pub = Column(String)
    img_url = Column(String)
    tag_id = Column(Integer, ForeignKey('tags.id'))

    tag = relationship('Tag', back_populates='books')

    def __repr__(self):
        return "<Book(name='%s', des='%s', pub='%s', img_url='%s')>" % (
            self.name, self.des,  self.pub, self.img_url
        )


class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)
    name = Column(String)


