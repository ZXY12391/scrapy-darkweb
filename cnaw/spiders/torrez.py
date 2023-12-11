import scrapy
import re
import datetime
from cnaw.items import CnawItem

import redis
from scrapy_redis.spiders import RedisSpider
from scrapy.linkextractors import LinkExtractor
from cnaw.spiders.basespider import BaseSpider
from cnaw.utils.test import check_existence
class TorrezSpider(BaseSpider,RedisSpider):
    name = "torrez"
    redis_key = "search_torrez"

    def parse(self, response):
        ul = response.xpath("//ul[@class='sidebar'][1]/li")
        for li in ul:
            href = li.xpath("./a/@href").extract_first()
            product_type = li.xpath("./a/text()").extract_first().strip()
            if product_type not in ['Drugs and Chemicals', 'Tutorials and e-books', 'Counterfeit']:
                yield scrapy.Request(
                    url=response.urljoin(href),
                    callback=self.parse_goods_url,
                )

    def parse_goods_url(self, response):


        # 解析商品URL和翻页逻辑

        trs = response.xpath("//table[@class='table table-custom table-listings']/tbody/tr")
        for tr in trs:
            href = tr.xpath("./td[2]/a/@href").extract_first()
            type1=tr.xpath("./td[2]/div/a[2]/text()").extract_first()
            type2=tr.xpath("./td[2]/div/a[3]/text()").extract_first()
            type=[]
            type.append(type1)
            type.append(type2)
            # 具体的商品URL解析逻辑
            yield scrapy.Request(
                url=response.urljoin(href),
                callback=self.parse_goods_detail,
                meta={
                    'type': type,
                }
            )

        # 翻页逻辑
        page_le = LinkExtractor(restrict_xpaths=("//a[@class='page-link']",))
        page_links = page_le.extract_links(response)
        for page in page_links:
            yield scrapy.Request(
                url=page.url,
                callback=self.parse_goods_url,
            )

    def parse_goods_detail(self, response):
        content = response.xpath("//div[@class='tab-pane active']/p/text()").extract_first()
        result = check_existence(content, 'Torrez')
        if result:
            url = response.url
            publish_time = None
            price = response.xpath("//span[@class='itemPrice']/text()").extract_first()
            types = response.meta.get('type')
            title = response.xpath("//div[@class='titleHeader mb-2'][1]/h3/text()").extract_first()
            source = "Torrez"
            fetch_time = datetime.datetime.now()
            yield self.saveData(source, types, title, content, price, publish_time, fetch_time, url)
