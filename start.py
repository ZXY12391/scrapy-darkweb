import scrapy
import datetime
from cnaw.items import CnawItem
from scrapy.linkextractors import LinkExtractor
from scrapy_redis.spiders import RedisSpider  # 导入 RedisSpider
from cnaw.settings import REDIS_HOST,REDIS_DB,REDIS_PARAMS,REDIS_PORT
import redis
class AsapSpider(RedisSpider):
    name = "asap"
    # start_urls = ["http://asap4g7boedkl3fxbnf2unnnr6kpxnwoewzw4vakaxiuzfdo5xpmy6ad.onion/search?categoryId=6a99b55b-8258-4aa8-b75e-678fd4cda86d"]
    redis_key = "search_url"
    def __init__(self, *args, **kwargs):
        super(AsapSpider, self).__init__(*args, **kwargs)
        url = 'http://asap4g7boedkl3fxbnf2unnnr6kpxnwoewzw4vakaxiuzfdo5xpmy6ad.onion/'
        # 请替换为您自己的Redis连接信息
        redis_host = REDIS_HOST
        redis_port = REDIS_PORT
        redis_db = REDIS_DB
        redis_password = REDIS_PARAMS.get('password')
        redis_conn = redis.StrictRedis(host=redis_host, password=redis_password, port=redis_port, db=redis_db)
        redis_conn.lpush('search_url', url)
    def parse(self, response):
        print(response.text)
        lis=response.xpath("(//ul[@class='nav-list'])[2]/li")
        for li in lis:
            if li.xpath("./section"):
                #href=li.xpath("./section/label/a/@href").extract_first()
                type=li.xpath("./section/label/a/text()").extract_first().strip()
            else:
                #href=li.xpath("./a/@href").extract_first()
                type=li.xpath("./a/text()").extract_first().strip()
            if type in ['Fraud','Digital goods']:
                #print(f"{type}:{href}")
                hrefs=li.xpath("./section/ul/li/a/@href").extract()
                for href in hrefs:
                    print(href)
                    """yield scrapy.Request(
                        url=response.urljoin(href),
                        callback=self.parse_good_url,
                    )"""

    """def parse_good_url(self,response):
        a = response.xpath("/html/body/div/div[2]/div/div[3]/div/form/div/div[1]/div[1]/div/span[1]/a/@href").extract()
        for href in a:
            print(response.urljoin(href))
            yield scrapy.Request(
                url=response.urljoin(href),
                callback=self.parse_goods_detail,
            )
            # 翻页
            page_le = LinkExtractor(restrict_xpaths=("//ul[@class='pagination']/li/a",))
            page_links = page_le.extract_links(response)
            for page in page_links:
                yield scrapy.Request(
                    url=response.urljoin(page.url),
                    callback=self.parse_good_url,
                )
    def parse_goods_detail(self,response):
        title = response.xpath("//div[@class='breadcrumbs']/h4/text()").extract_first()
        type = 'Fraud'
        if response.xpath("/html/body/div/div[2]/div/div[2]/table/tbody/tr/td/table/tbody/tr[5]/td/a[2]/text()").extract_first():
            type = response.xpath("/html/body/div/div[2]/div/div[2]/table/tbody/tr/td/table/tbody/tr[5]/td/a[2]/text()").extract_first()
        content = response.xpath("//div[@class='white-space-formatted'][1]/text()").extract_first()
        publish = None
        fetch_time = datetime.datetime.now()
        source = 'Asap'
        url = response.url
        price = response.xpath("/html/body/div/div[2]/div/div[2]/table/tbody/tr/td/table/tbody/tr[1]/td/text()").extract_first()
        item = CnawItem()
        item['Source'] = source
        item['Type'] = type
        item['Title'] = title
        item['Content'] = content
        item['Price'] = price
        item['Publish_time'] = publish
        item['Fetch_time'] = fetch_time
        item['Url'] = url
        yield item"""