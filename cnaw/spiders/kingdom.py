import scrapy
import re
import datetime
from cnaw.items import CnawItem
from scrapy.linkextractors import LinkExtractor
from cnaw.settings import REDIS_HOST,REDIS_DB,REDIS_PARAMS,REDIS_PORT
import redis
class KingdomSpider(scrapy.Spider):
    name = "kingdom"

    #start_urls = ["https://kingdom4it4wzkkud2p2esvashyynvmsrbyuk4qh2bnyvcnoafyvoiyd.onion.is/?t=31832a84d397c3c1"]
    redis_key = "search_url"

    def __init__(self, *args, **kwargs):
        super(KingdomSpider, self).__init__(*args, **kwargs)
        url = 'https://kingdom4it4wzkkud2p2esvashyynvmsrbyuk4qh2bnyvcnoafyvoiyd.onion.is/?t=31832a84d397c3c1'
        # 请替换为您自己的Redis连接信息
        redis_host = REDIS_HOST
        redis_port = REDIS_PORT
        redis_db = REDIS_DB
        redis_password = REDIS_PARAMS.get('password')
        redis_conn = redis.StrictRedis(host=redis_host, password=redis_password, port=redis_port, db=redis_db)
        redis_conn.lpush('search_url', url)

    def parse(self, response):
       # print(response.text)
        uls=response.xpath("(//div[@class='sidebar'])[3]/ul")
        #print(uls)
        for ul in uls:
            type=ul.xpath("./a/text()").extract_first().strip()
            type = re.sub(r'\(\d+\)', '', type).strip()
            #print(type)
            if type not in ['Drugs', 'Jewellery & Art', 'Counterfeit']:
                href = ul.xpath("./a/@href").extract_first()
                #print(response.urljoin(href))
                yield scrapy.Request(
                        url=response.urljoin(href),
                        callback=self.parse_good_url,
                        meta={
                            'type': type,
                        }
                    )

    def parse_good_url(self,response):
        print(f"访问第{response.url}页")
        type=response.meta.get('type')
        #置顶的为毒药药片
        """divs=response.xpath("//div[@class='box-cont']/div[@class='row']/div")
        for div in divs:
            href=div.xpath("./div/div/a/@href").extract_first()
            print(f"{type}:{href}")
            yield scrapy.Request(
                url=response.urljoin(href),
                callback=self.parse_good_detail,
                meta={
                    'type': type,
                }
            )"""
        div2s=response.xpath("//div[@id='p0']/div/div")
        for div in div2s:
            href=div.xpath("./div[@class='col-md-7']/a[1]/@href").extract_first()
            print(f"{type}:{href}")
            yield scrapy.Request(
                url=response.urljoin(href),
                callback=self.parse_good_detail,
                meta={
                    'type': type,
                }
            )
            # 翻页
            page_le = LinkExtractor(restrict_xpaths=("//ul[@class='pagination']/li/a",))
            page_links = page_le.extract_links(response)
            for page in page_links:
                yield scrapy.Request(
                    url=response.urljoin(page.url),
                    callback=self.parse_good_url,
                    meta={
                        'type': type,
                    }
                )

    def parse_good_detail(self,response):
        type = response.meta.get('type')
        title_elements = response.xpath("/html/body/div/div/div[3]/div[2]/form/div[2]/div[1]/text()").extract()
        # 使用join()方法将文本元素合并为一个字符串
        title = ''.join(title_elements)
        title=title.strip()
        content = response.xpath("//*[@id='descriptionContent']/text()").extract_first()
        price = response.xpath("(//div[@class='col-md-8'])[2]/div[@class='box-cont']/div/div[last()]/text()").extract_first()
        publish_time=response.xpath("/html/body/div/div/div[3]/div[2]/form/div[2]/div[2]/div[1]/div[14]/text()").extract_first()
        fetch_time = datetime.datetime.now()
        source = 'kingdom'
        url = response.url
        #print(f"已经爬取{type}的商品{url}")
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




