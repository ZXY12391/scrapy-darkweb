import scrapy
from cnaw.items import CnawItem
import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy_redis.spiders import RedisSpider  # 导入 RedisSpider
from cnaw.settings import REDIS_HOST,REDIS_DB,REDIS_PARAMS,REDIS_PORT,get_redis_connection
import redis
from cnaw.spiders.basespider import BaseSpider
class NemesisSpider(BaseSpider,RedisSpider):
    name = "nemesis"
    redis_key = "search_nemesis"
    def parse(self, response):
        #print(response.text)
        lis=response.xpath("//ul[@class='navbar-nav me-auto']/li")
        for li in lis:
            type = li.xpath("./a/text()").extract_first().strip()
            print(type)
            if type not in ['Drugs', 'Forgeries/Counterfeits']:
                href=li.xpath("./a/@href").extract_first()
                print(response.urljoin(href))
                yield scrapy.Request(
                               url=response.urljoin(href),
                               callback=self.parse_goods_url,
                )
    def parse_goods_url(self,response):
        divs=response.xpath("//div[@class='row g-5 g-xl-5']/div")
        for div in divs:
            href=div.xpath("./div/div[1]/div[2]/a/@href").extract_first()
            #print(response.urljoin(href))
            yield scrapy.Request(
                url=response.urljoin(href),
                callback=self.parse_goods_detail,
            )
        #翻页
        page_le = LinkExtractor(restrict_xpaths=("//ul[@class='pagination']/li/a",))
        page_links = page_le.extract_links(response)
        for page in page_links:
            yield scrapy.Request(
                url=response.urljoin(page.url),
                callback=self.parse_goods_url,
            )

    def parse_goods_detail(self,response):
        title=response.xpath("//a[@class='fs-1 text-gray-800 fw-bolder me-3 mb-3']/text()").extract_first()
        text_content = response.xpath("//div[@class='fs-5 text-gray-800'][1]//text()").extract()
        content = ' '.join(text_content)
        publish=response.xpath("//div[@class='fs-7 text-gray-400']//text()").extract()
        publish_time = ' '.join(publish)
        price=None
        if response.xpath("//div[@class='text-gray-800 fs-1 fw-bolder mt-6']/text()").extract_first():
            price=response.xpath("//div[@class='text-gray-800 fs-1 fw-bolder mt-6']/text()").extract_first()
        fetch_time = datetime.datetime.now()
        source = 'Nemesis'
        url = response.url
        type1 = response.xpath("//div[@class='fs-7 py-1']/a[1]/text()").extract_first()
        type2 = response.xpath("//div[@class='fs-7 py-1']/a[2]/text()").extract_first()
        types = []
        types.append(type1)
        types.append(type2)
        yield self.saveData(source, types, title, content, price, publish_time, fetch_time, url)










