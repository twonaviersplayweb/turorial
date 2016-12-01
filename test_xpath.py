#!/usr/bin/env python
# coding=utf-8

import codecs
from lxml import etree

f = codecs.open('book.html', 'r', 'utf-8')
content = f.read()
f.close()
tree = etree.HTML(content)
