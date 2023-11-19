import scrapy
from cnaw.items import CnawItem
import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy_redis.spiders import RedisSpider  # 导入 RedisSpider
from cnaw.settings import REDIS_HOST,REDIS_DB,REDIS_PARAMS,REDIS_PORT
import redis
class NemesisSpider(RedisSpider):
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
                               callback=self.parse_good_url,
                )
    def parse_good_url(self,response):
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
                callback=self.parse_good_url,
            )

    def parse_goods_detail(self,response):
        title=response.xpath("//a[@class='fs-1 text-gray-800 fw-bolder me-3 mb-3']/text()").extract_first()
        text_content = response.xpath("//div[@class='fs-5 text-gray-800'][1]//text()").extract()
        content = ' '.join(text_content)
        publish=response.xpath("//div[@class='fs-7 text-gray-400']//text()").extract()
        publish_time = ' '.join(publish)
        price_one=None
        prices = []
        if response.xpath("//div[@class='text-gray-800 fs-1 fw-bolder mt-6']/text()").extract_first():
            price_one=response.xpath("//div[@class='text-gray-800 fs-1 fw-bolder mt-6']/text()").extract_first().strip()
        else:
            labels=response.xpath("//div[@class='mt-6']/label")
            for label in labels:
                price_1=label.xpath(".//text()").extract()
                price = ' '.join(price_1)
                price=price.strip()
                prices.append(price)
        fetch_time = datetime.datetime.now()
        source = 'Nemesis'
        url = response.url
        type1 = response.xpath("//div[@class='fs-7 py-1']/a[1]/text()").extract_first()
        type2 = response.xpath("//div[@class='fs-7 py-1']/a[2]/text()").extract_first()
        type = []
        type.append(type1)
        type.append(type2)
        item = CnawItem()
        item['Source'] = source
        item['Type'] = type
        item['Title'] = title
        item['Content'] = content
        if price_one:
            item['Price'] = price_one
        else:
            item['Price'] = prices
        item['Publish_time'] = publish_time
        item['Fetch_time'] = fetch_time
        item['Url'] = url
        yield item











