import scrapy
import re
import datetime
from cnaw.items import CnawItem
from scrapy.linkextractors import LinkExtractor
from cnaw.settings import REDIS_HOST,REDIS_DB,REDIS_PARAMS,REDIS_PORT,get_redis_connection
from scrapy_redis.spiders import RedisSpider  # 导入 RedisSpider
import redis
import os
class KingdomSpider(RedisSpider):
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
                        callback=self.parse_good_url,
                        meta={
                            'type': type,
                        }

                    )

    def parse_good_url(self,response):
        type1=response.meta.get('type')
        div2s=response.xpath("//div[@id='p0']/div/div")
        for div in div2s:
            href=div.xpath("./div[@class='col-md-7']/a[1]/@href").extract_first()
            type2=div.xpath("./div[@class='col-md-7']/a[2]/text()").extract_first()
            #print(f"{type}:{href}")
            yield scrapy.Request(
                url=response.urljoin(href),
                callback=self.parse_good_detail,
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
                    callback=self.parse_good_url,
                    meta={
                        'type': type1,
                    }
        )

    def parse_good_detail(self,response):
        type1=response.meta.get('type1')
        type2 = response.meta.get('type2')
        type = []
        type.append(type1)
        type.append(type2)
        title_elements = response.xpath("/html/body/div/div/div[3]/div[2]/form/div[2]/div[1]/text()").extract()
        # 使用join()方法将文本元素合并为一个字符串
        title = ''.join(title_elements)
        title=title.strip()
        if not title:
            # 如果标题为空，将HTML内容保存到本地
            self.save_html_to_file(response, f'empty_title{self.num}.html')
            self.num=self.num+1
            #print(response.text)
        content = response.xpath("//*[@id='descriptionContent']/text()").extract_first()
        price = response.xpath("(//div[@class='col-md-8'])[2]/div[@class='box-cont']/div/div[last()]/text()").extract_first()
        publish_time=response.xpath("/html/body/div/div/div[3]/div[2]/form/div[2]/div[2]/div[1]/div[14]/text()").extract_first()
        fetch_time = datetime.datetime.now()
        source = 'Kingdom'
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

    def save_html_to_file(self, response, filename):
        # 文件保存目录
        save_dir = 'html_debug/'
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        # 构建完整的文件路径
        file_path = os.path.join(save_dir, filename)

        # 保存HTML内容到文件
        with open(file_path, 'wb') as file:
            file.write(response.body)



