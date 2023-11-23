import scrapy
import datetime
from cnaw.items import CnawItem
from scrapy.linkextractors import LinkExtractor
from scrapy_redis.spiders import RedisSpider  # 导入 RedisSpider
from cnaw.settings import REDIS_HOST,REDIS_DB,REDIS_PARAMS,REDIS_PORT,get_redis_connection
import redis
from cnaw.spiders.basespider import BaseSpider
class MgmgrandSpider(BaseSpider,RedisSpider):
    name = "MGMGrand"
    redis_key = "search_MgmGrand"
    def parse(self, response):
        #print(response.text)
        #print(response.text)
        lis=response.xpath("//ul[@class='categories-menu d-flex justify-content-center flex-wrap']/li")
        for li in lis:
            href=li.xpath("./a/@href").extract_first()
            types=li.xpath("./a/text()").extract()
            type=''.join(types)
            type=type.strip()
            print(f"{type}:{href}")
            if type not in ['Drugs']:
                yield scrapy.Request(
                    url=response.urljoin(href),
                    callback=self.parse_goods_url,
                )
    def parse_goods_url(self,response):
        divs=response.xpath("//div[@class='list-products  columns-3']/div")
        for div in divs:
            href=div.xpath("./div[1]/a/@href").extract_first()
            yield scrapy.Request(
                url=response.urljoin(href),
                callback=self.parse_goods_detail,
            )
            # 翻页
            page_le = LinkExtractor(restrict_xpaths=("//ul[@class='pagination mb-0']/li/a",))
            page_links = page_le.extract_links(response)
            for page in page_links:
                yield scrapy.Request(
                    url=response.urljoin(page.url),
                    callback=self.parse_goods_url,
                )

    def parse_goods_detail(self,response):
        title = response.xpath("//h1[@class='normal-title c-fs-3']/text()").extract_first()
        type1 = response.xpath("//div[@class='c-breadcrumb']/a[3]/text()").extract_first()
        type2 = response.xpath("//div[@class='c-breadcrumb']/a[4]/text()").extract_first()
        types=[]
        types.append(type1)
        types.append(type2)
        content = response.xpath("//div[@class='tab-pane fade  show active ']/pre/text()").extract_first()
        publish_time = None
        fetch_time = datetime.datetime.now()
        source = 'MGMGrand'
        url = response.url
        price = response.xpath("//span[@class='col-5']/strong/text()").extract_first()
        yield self.saveData(source, types, title, content, price, publish_time, fetch_time, url)







