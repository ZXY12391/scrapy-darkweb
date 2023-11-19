import scrapy
import datetime
from cnaw.items import CnawItem
from scrapy.linkextractors import LinkExtractor
from scrapy_redis.spiders import RedisSpider  # 导入 RedisSpider
from cnaw.settings import REDIS_HOST,REDIS_DB,REDIS_PARAMS,REDIS_PORT,get_redis_connection
import redis
class AsapSpider(RedisSpider):
    name = "asap"
    # start_urls = ["http://asap4g7boedkl3fxbnf2unnnr6kpxnwoewzw4vakaxiuzfdo5xpmy6ad.onion/search?categoryId=6a99b55b-8258-4aa8-b75e-678fd4cda86d"]
    redis_key = "search_asap"

    def parse(self, response):
        #print(response.text)
        lis=response.xpath("(//ul[@class='nav-list'])[2]/li")
        for li in lis:
            if li.xpath("./section"):
                #href=li.xpath("./section/label/a/@href").extract_first()
                type=li.xpath("./section/label/a/text()").extract_first().strip()
            else:
                #href=li.xpath("./a/@href").extract_first()
                type=li.xpath("./a/text()").extract_first().strip()
            #print(type)
            if type in ['Fraud','Digital goods']:
                #print(f"{type}:{href}")
                hrefs=li.xpath("./section/ul/li/a/@href").extract()
                for href in hrefs:
                    #print(href)
                    yield scrapy.Request(
                        url=response.urljoin(href),
                        callback=self.parse_good_url,
                    )

    def parse_good_url(self, response):
        a=response.xpath("//div[@class='clr-col-lg-4 clr-col-md-6 card-search-listing']//span[@class='card-media-title']/a/@href").extract()
        for href in a:
            #print(response.urljoin(href))
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

    def parse_goods_detail(self, response):
        title = response.xpath("//div[@class='breadcrumbs']/h4/text()").extract_first()
        type1 = response.xpath("(//table[@class='table table-vertical table-noborder table-compact table-no-margin'])[2]/tbody/tr[5]/td/a[1]/text()").extract_first()
        type2 = response.xpath("(//table[@class='table table-vertical table-noborder table-compact table-no-margin'])[2]/tbody/tr[5]/td/a[2]/text()").extract_first()
        type=[]
        type.append(type1)
        type.append(type2)
        content = response.xpath("//div[@class='white-space-formatted'][1]/text()").extract_first()
        publish = None
        fetch_time = datetime.datetime.now()
        source = 'Asap'
        url = response.url
        price = response.xpath(
            "(//table[@class='table table-vertical table-noborder table-compact table-no-margin'])[2]/tbody/tr[1]/td/text()").extract_first()
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
