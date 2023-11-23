import scrapy
import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy_redis.spiders import RedisSpider  # 导入 RedisSpider
from cnaw.spiders.basespider import BaseSpider

class AsapSpider(BaseSpider, RedisSpider):
    name = "asap"
    redis_key = "search_asap"
    def parse(self, response):
        lis = response.xpath("(//ul[@class='nav-list'])[2]/li")
        for li in lis:
            if li.xpath("./section"):
                type = li.xpath("./section/label/a/text()").extract_first().strip()
            else:
                type = li.xpath("./a/text()").extract_first().strip()

            if type in ['Fraud', 'Digital goods']:
                hrefs = li.xpath("./section/ul/li/a/@href").extract()
                for href in hrefs:
                    yield scrapy.Request(
                        url=response.urljoin(href),
                        callback=self.parse_goods_url,
                    )

    def parse_goods_url(self, response):
        a = response.xpath("//div[@class='clr-col-lg-4 clr-col-md-6 card-search-listing']//span[@class='card-media-title']/a/@href").extract()
        for href in a:
            yield scrapy.Request(
                url=response.urljoin(href),
                callback=self.parse_goods_detail,
            )

        # 翻页放在外部循环之后
        page_le = LinkExtractor(restrict_xpaths=("//ul[@class='pagination']/li/a",))
        page_links = page_le.extract_links(response)
        for page in page_links:
            yield scrapy.Request(
                url=response.urljoin(page.url),
                callback=self.parse_goods_url,
            )

    def parse_goods_detail(self, response):
        title = response.xpath("//div[@class='breadcrumbs']/h4/text()").extract_first()
        type1 = response.xpath("(//table[@class='table table-vertical table-noborder table-compact table-no-margin'])[2]/tbody/tr[5]/td/a[1]/text()").extract_first()
        type2 = response.xpath("(//table[@class='table table-vertical table-noborder table-compact table-no-margin'])[2]/tbody/tr[5]/td/a[2]/text()").extract_first()
        types = []
        types.append(type1)
        types.append(type2)
        content = response.xpath("//div[@class='white-space-formatted'][1]/text()").extract_first()
        publish_time = None
        fetch_time = datetime.datetime.now()
        source = 'Asap'
        url = response.url
        price = response.xpath(
            "(//table[@class='table table-vertical table-noborder table-compact table-no-margin'])[2]/tbody/tr[1]/td/text()").extract_first()
        yield self.saveData(source, types, title, content, price, publish_time, fetch_time, url)
