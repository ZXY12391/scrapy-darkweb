import scrapy
import re
import datetime
from cnaw.items import CnawItem
from cnaw.settings import REDIS_DB, REDIS_HOST, REDIS_PORT
import redis
from scrapy_redis.spiders import RedisSpider
from scrapy.linkextractors import LinkExtractor

class TorrezSpider(RedisSpider):
    name = "torrez"
    redis_key = "search_url"
    good_num1 = {}
    good_num2 = {}

    def __init__(self, *args, **kwargs):
        super(TorrezSpider, self).__init__(*args, **kwargs)
        self.page_count = {}  # 创建一个字典用于存储每种商品类型的页码计数
        url = 'http://mmd32xdcmzrdlpoapkpf43dxig5iufbpkkl76qnijgzadythu55fvkqd.onion/home'
        redis_host = REDIS_HOST
        redis_port = REDIS_PORT
        redis_db = REDIS_DB
        redis_conn = redis.StrictRedis(host=redis_host, port=redis_port, db=redis_db)
        redis_conn.lpush('search_url', url)

    def parse(self, response):
        ul = response.xpath("//ul[@class='sidebar'][1]/li")
        for li in ul:
            href = li.xpath("./a/@href").extract_first()
            product_type = li.xpath("./a/text()").extract_first().strip()

            if product_type not in ['Drugs and Chemicals', 'Tutorials and e-books', 'Counterfeit']:
                # 初始化页码计数值和两个商品计数值为0
                self.page_count[product_type] = 0
                self.good_num1[product_type] = 0
                self.good_num2[product_type] = 0
                yield scrapy.Request(
                    url=response.urljoin(href),
                    callback=self.parse_goods_url,
                    meta={
                        'type': product_type,
                    }
                )

    def parse_goods_url(self, response):
        product_type = response.meta.get('type')
        # 增加页码计数值
        self.page_count[product_type] += 1
        current_page = self.page_count[product_type]
        print(f"Scraping {product_type}, Page {current_page}: {response.url}")

        # 解析商品URL和翻页逻辑

        trs = response.xpath("//table[@class='table table-custom table-listings']/tbody/tr")
        for tr in trs:
            href = tr.xpath("./td[2]/a/@href").extract_first()
            # 增加已抓取商品计数值
            self.good_num1[product_type] += 1
            current_good_num1 = self.good_num1[product_type]
            print(f"{product_type}: 第{current_good_num1}个准备抓取商品：{response.urljoin(href)}")
            # 具体的商品URL解析逻辑
            yield scrapy.Request(
                url=response.urljoin(href),
                callback=self.parse_goods_detail,
                meta={
                    'type': product_type,
                }
            )

        # 翻页逻辑
        page_le = LinkExtractor(restrict_xpaths=("//a[@class='page-link']",))
        page_links = page_le.extract_links(response)
        for page in page_links:
            yield scrapy.Request(
                url=page.url,
                callback=self.parse_goods_url,
                meta={
                    'type': product_type,
                }
            )

    def parse_goods_detail(self, response):
        publish_time = None
        price = response.xpath("//span[@class='itemPrice']/text()").extract_first()
        product_type = response.meta.get('type')
        title = response.xpath("//div[@class='titleHeader mb-2'][1]/h3/text()").extract_first()
        url = response.url
        content = response.xpath("//div[@class='tab-pane active']/p/text()").extract_first()
        source = "torrez"
        item = CnawItem()
        item['Source'] = source
        item['Type'] = product_type
        item['Title'] = title
        item['Content'] = content
        item['Price'] = price
        item['Publish_time'] = publish_time
        item['Fetch_time'] = datetime.datetime.now()
        item['Url'] = url
        # 增加未抓取商品计数值
        self.good_num2[product_type] += 1
        current_good_num2 = self.good_num2[product_type]
        print(f"{product_type}: 第{current_good_num2}个实际抓取商品：{url}")
        yield item
