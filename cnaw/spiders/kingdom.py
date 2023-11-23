import scrapy
import re
import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy_redis.spiders import RedisSpider  # 导入 RedisSpider
from cnaw.spiders.basespider import BaseSpider
class KingdomSpider(BaseSpider,RedisSpider):
    name = "kingdom"
    num=0
    #start_urls = ["https://kingdom4it4wzkkud2p2esvashyynvmsrbyuk4qh2bnyvcnoafyvoiyd.onion.is/?t=31832a84d397c3c1"]
    redis_key = "search_kingdom"
    def parse(self, response):
        #print(response.text)
        uls=response.xpath("(//div[@class='sidebar'])[3]/ul")
        #print(uls)
        for ul in uls:
            type = ul.xpath("./a[1]/text()").extract_first().strip()
            type = re.sub(r'\(\d+\)', '', type).strip()
            print(type)
            if type not in ['Drugs', 'Jewellery & Art', 'Counterfeit']:
                href = ul.xpath("./a[1]/@href").extract_first()
                #print(response.urljoin(href))
                yield scrapy.Request(
                        url=response.urljoin(href),
                        callback=self.parse_goods_url,
                        meta={
                            'type': type,
                        }

                    )

    def parse_goods_url(self,response):
        type1=response.meta.get('type')
        div2s=response.xpath("//div[@id='p0']/div/div")
        for div in div2s:
            href=div.xpath("./div[@class='col-md-7']/a[1]/@href").extract_first()
            type2=div.xpath("./div[@class='col-md-7']/a[2]/text()").extract_first()
            #print(f"{type}:{href}")
            yield scrapy.Request(
                url=response.urljoin(href),
                callback=self.parse_goods_detail,
                meta={
                    'type1': type1,
                    'type2':type2
                }
            )
            #type.clear()
            # 翻页
        page_le = LinkExtractor(restrict_xpaths=("//ul[@class='pagination']/li/a",))
        page_links = page_le.extract_links(response)
        for page in page_links:
            yield scrapy.Request(
                    url=response.urljoin(page.url),
                    callback=self.parse_goods_url,
                    meta={
                        'type': type1,
                    }
        )

    def parse_goods_detail(self,response):
        type1=response.meta.get('type1')
        type2 = response.meta.get('type2')
        types = []
        types.append(type1)
        types.append(type2)
        title_elements = response.xpath("/html/body/div/div/div[3]/div[2]/form/div[2]/div[1]/text()").extract()
        # 使用join()方法将文本元素合并为一个字符串
        title = ''.join(title_elements)
        title=title.strip()
        content = response.xpath("//*[@id='descriptionContent']/text()").extract_first()
        price = response.xpath("(//div[@class='col-md-8'])[2]/div[@class='box-cont']/div/div[last()]/text()").extract_first()
        publish_time=response.xpath("/html/body/div/div/div[3]/div[2]/form/div[2]/div[2]/div[1]/div[14]/text()").extract_first()
        fetch_time = datetime.datetime.now()
        source = 'Kingdom'
        url = response.url
        #print(f"已经爬取{type}的商品{url}")
        yield self.saveData(source, types, title, content, price, publish_time, fetch_time, url)

    
