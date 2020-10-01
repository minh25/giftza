# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo
import json


class GiftzaPipeline:
    def process_item(self, item, spider):
        return item


class MongoPipeline:
    '''
    Push the collected data to mongoDB

    Setting:
    mongo_collection: giftza.pipelines.MongoPipeline.process_item.mongo_collection
    MONGO_URI: giftza.settings.MONGO_URI
    MONGO_DATABASE: giftza.settings.MONGO_DATABASE
    '''

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        mongo_collection = 'scrapy_items'
        self.db[mongo_collection].update_one({'campaignId': item['campaignId']},
                                                 {'$set': ItemAdapter(item).asdict()},
                                                 upsert=True)
        return item


class JsonWriterPipeline:
    '''
    Write the data of product
    - code
    - url
    - decription
    - name
    - price
    - url of the main image
    to a json file.

    Setting:
    file_name: giftza.pipelines.JsonWritePipeline.open_spider.file_name
    '''

    def open_spider(self, spider):

        # name of json file
        file_name = 'items.json'

        self.file = open(file_name, 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(ItemAdapter(item).asdict()) + "\n"
        self.file.write(line)
        return item

class CsvWriterPipeline:
    '''
    Write the data of product
    - code
    - url
    - decription
    - name
    - price
    - url of the main image
    to a csv file.

    Setting:
    file_name: giftza.pipelines.CsvWritePipeline.open_spider.file_name
    '''

    def open_spider(self, spider):

        # name of csv file
        file_name = 'items.csv'

        self.file = open(file_name, 'w')
        line = 'code, url, description, name, price, image\n'
        self.file.write(line)

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        item_json = ItemAdapter(item).asdict()
        line = ''
        for x, y in item_json.items():
            line += str(y) + ', '
        line += '\n'
        self.file.write(line)
        return item
