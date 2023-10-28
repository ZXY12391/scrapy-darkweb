# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import pymongo
from cnaw.settings import MongoDB
class CnawPipeline:
    """
       我们希望在爬虫开始时，打开这个文件
       在执行过程中，不断往里存储数据
       执行完毕时，关闭这个文件
       """
    num=0
    def open_spider(self, spider):
        self.client = pymongo.MongoClient(host=MongoDB['host'], port=MongoDB['port'])
        db = self.client['local']
        #  db.authenticate("local","123456")
        self.collection = db[MongoDB['collection']]  # 这个collection只需为空即可，不用创建列什么的

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):

        self.collection.insert_one({"Source": item['Source'],
                                    "Type": item['Type'],
                                    "Title": item['Title'],
                                    "Content": item['Content'],
                                    "Price": item['Price'],
                                    "Publish_time": item['Publish_time'],
                                    "Fetch_time": item['Fetch_time'],
                                    "Url": item['Url'],
                                    })
        # print(item)
        return item