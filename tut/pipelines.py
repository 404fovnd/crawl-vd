# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import codecs
import pymongo

class TutPipeline(object):

    def __init__(self):
        #self.file = codecs.open('cnvd.json', mode = 'wb', encoding = 'utf-8')
        self.connection = pymongo.MongoClient('localhost', 27017)
        self.db = self.connection.vul_database
        self.col = self.db.cnvd
        

    def process_item(self, item, spider):

        data = dict(item)
        self.col.save({'title': data['title'], 'cnvdid': data['cnvdid'],
                'pub_date':data['pub_date']})

        #line = json.dumps(dict(item)) + '\n'

        #self.file.write(line.decode('unicode_escape'))
        #l = line.decode('unicode_escape')
        return item
