import scrapy
import datetime
from cnaw.items import CnawItem
from scrapy.linkextractors import LinkExtractor
from scrapy_redis.spiders import RedisSpider  # 导入 RedisSpider
from cnaw.settings import REDIS_HOST,REDIS_DB,REDIS_PARAMS,REDIS_PORT
import redis
class MgmgrandSpider(RedisSpider):
    name = "MGMGrand"
    #start_urls = ["http://duysanjqxo4svh35yqkxxe5r54z2xc5tjf6r3ichxd3m2rwcgabf44ad.onion/#subscribe-modal"]
    redis_key = "search_MgmGrand"
    def __init__(self, *args, **kwargs):
        super( MgmgrandSpider, self).__init__(*args, **kwargs)
        url = 'http://duysanjqxo4svh35yqkxxe5r54z2xc5tjf6r3ichxd3m2rwcgabf44ad.onion/#subscribe-modal'
        # 请替换为您自己的Redis连接信息
        redis_host = REDIS_HOST
        redis_port = REDIS_PORT
        redis_db = REDIS_DB
        redis_password = REDIS_PARAMS.get('password')
        redis_conn = redis.StrictRedis(host=redis_host, password=redis_password, port=redis_port, db=redis_db)
        redis_conn.lpush('search_url', url)

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
                    callback=self.parse_good_url,
                )
    def parse_good_url(self,response):
        divs=response.xpath("//div[@class='list-products  columns-3']/div")
        for div in divs:
            href=div.xpath("./div[1]/a/@href").extract_first()
            yield scrapy.Request(
                url=response.urljoin(href),
                callback=self.parse_good_deatil,
            )
            # 翻页
            page_le = LinkExtractor(restrict_xpaths=("//ul[@class='pagination mb-0']/li/a",))
            page_links = page_le.extract_links(response)
            for page in page_links:
                yield scrapy.Request(
                    url=response.urljoin(page.url),
                    callback=self.parse_good_url,
                )

    def parse_good_deatil(self,response):
        title = response.xpath("//h1[@class='normal-title c-fs-3']/text()").extract_first()
        type1 = response.xpath("//div[@class='c-breadcrumb']/a[3]/text()").extract_first()
        type2 = response.xpath("//div[@class='c-breadcrumb']/a[4]/text()").extract_first()
        type=[]
        type.append(type1)
        type.append(type2)
        content = response.xpath("//div[@class='tab-pane fade  show active ']/pre/text()").extract_first()
        publish = None
        fetch_time = datetime.datetime.now()
        source = 'MGMGrand'
        url = response.url
        price = response.xpath("//span[@class='col-5']/strong/text()").extract_first()
        item = CnawItem()
        item['Source'] = source
        item['Type'] = type
        item['Title'] = title
        item['Content'] = content
        item['Price'] = price
        item['Publish_time'] = publish
        item['Fetch_time'] = fetch_time
        item['Url'] = url
        yield item







