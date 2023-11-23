import scrapy
from abc import ABC, abstractmethod
import datetime
from cnaw.items import CnawItem  # 确保引入正确的包

class BaseSpider(scrapy.Spider, ABC):
    name = 'base_spider'

    @abstractmethod
    def parse(self, response):
        pass

    @abstractmethod
    def parse_goods_url(self, response):
        pass

    @abstractmethod
    def parse_goods_detail(self, response):
        pass

    def saveData(self, source, types, title, content, price, publish, fetch_time, url):
        item = CnawItem()
        item['Source'] = source
        item['Type'] = types
        item['Title'] = title
        item['Content'] = content
        item['Price'] = price
        item['Publish_time'] = publish
        item['Fetch_time'] = fetch_time
        item['Url'] = url
        return item
