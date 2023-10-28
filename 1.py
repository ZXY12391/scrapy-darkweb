import scrapy
import re
import datetime
from cnaw.items import CnawItem
from cnaw.settings import REDIS_DB,REDIS_HOST,REDIS_PORT,REDIS_PARAMS
import redis
from scrapy_redis.spiders import RedisSpider  # 导入 RedisSpider
from scrapy.linkextractors import  LinkExtractor
class TorrezSpider(RedisSpider):
    name = "torrez"
    redis_key = "search_url"
    def __init__(self, *args, **kwargs):
        super(TorrezSpider, self).__init__(*args, **kwargs)
        url = 'http://mmd32xdcmzrdlpoapkpf43dxig5iufbpkkl76qnijgzadythu55fvkqd.onion/home'
        # 请替换为您自己的Redis连接信息
        redis_host = REDIS_HOST
        redis_port = REDIS_PORT
        redis_db = REDIS_DB
        redis_password = REDIS_PARAMS.get('password')
        redis_conn = redis.StrictRedis(host=redis_host, password=redis_password, port=redis_port, db=redis_db)
        redis_conn.lpush('search_url', url)

    def parse(self, response):
        #print(response.text)
        ul=response.xpath("//ul[@class='sidebar'][1]/li")
        for li in ul:
            href=li.xpath("./a/@href").extract_first()
            type=li.xpath("./a/text()").extract_first()
            type = type.strip()
            #num=li.xpath("./a/span/text()").extract_first()
            #print(f"{type}:{href}")
            #print(num)
            yield scrapy.Request(
                url=response.urljoin(href),
                callback=self.parse_goods_url,
                meta={
                    'type':type
                }
            )


    def parse_goods_url(self,response):
        #print(response.url)
        type = response.meta.get('type')
        #解析每页的每个商品的URL
        trs = response.xpath("//table[@class='table table-custom table-listings']/tbody/tr")
        for tr in trs:
            href = tr.xpath("./td[2]/a/@href").extract_first()
            title = tr.xpath("./td[2]/a/text()").extract_first()
            # print(f"{title}:{href}")
            yield scrapy.Request(
                url=response.urljoin(href),
                callback=self.parse_goods_detail,
                meta={
                    'type': type
                }
            )
            # 翻页
        page_le = LinkExtractor(restrict_xpaths=("//a[@class='page-link']",))
        page_links = page_le.extract_links(response)
        print(page_links)
        for page in page_links:
            print(page.url)
            yield scrapy.Request(
            url=page.url,  # 有重复的URL没关系，scrapy会帮我们自动去重
            callback=self.parse_goods_url  # 循环上述操作
            )

    def parse_goods_detail(self,response):
        publish_time = None
        price_with_dollar_sign = response.xpath("//span[@class='itemPrice']/text()").extract_first()
        price = price_with_dollar_sign.replace("$", "")
        fetch_time = datetime.datetime.now()
        type = response.meta.get('type')
        title = response.xpath("//div[@class='titleHeader mb-2'][1]/h3/text()").extract_first()
        url = response.url
        content=response.xpath("//div[@class='tab-pane active']/p/text()").extract_first()
        source = "torrez"
        item = CnawItem()
        item['Source'] = source
        item['Type'] = type
        item['Title'] = title
        item['Content'] = content
        item['Price'] = price
        item['Publish_time'] = publish_time
        item['Fetch_time'] = fetch_time
        item['Url'] = url
        yield item





