import scrapy
import os
import datetime
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from cnaw.items import CnawItem
import redis
from scrapy_redis.spiders import RedisSpider  # 导入 RedisSpider
from cnaw.settings import REDIS_DB,REDIS_HOST,REDIS_PORT,REDIS_PARAMS
class ZwawwSpider(RedisSpider):
    name = "zwaww"
    redis_key = 'search_zwaww'
    def parse(self, response):
        print(response.text)
        print(response.url)
        divs = response.xpath("//div[@class='div_index_both'][2]/div")
        for div in divs:
            # print(div)
            # type=div.xpath("./table/tr/td/text()").extract_first()
            # print(type)
            # 查看更多链接
            href = div.xpath("./table/tr/td/div/a/@href").extract_first()
            # print(href)
            yield scrapy.Request(
                url=href,
                callback=self.parse_by1,  # 按照发布时间
            )
    def parse_by1(self, response):
        # 提取页面上的总页数
        pages = response.xpath("/html/body/div/div[3]/table/tr[1]/td/div/a[last()]/button/text()").extract_first()
        max_page = int(pages)
        print(max_page)

        # 计算中间页码
        jump_to_page = str(max_page // 2)
        print(f"中间页为 {jump_to_page}")

        # 提取所有的a标签
        hrefs = response.xpath("/html/body/div/div[3]/table/tr[1]/td/div/a")

        # 遍历a标签，找到对应按钮文本的a标签并提取href
        url = None
        for href in hrefs:
            button_text = href.xpath("./button/text()").extract_first().strip()
            if button_text == jump_to_page:
                url = href.xpath("@href").extract_first()
                break
        if url:
            # 生成一个随机参数，追加到URL中，如果你正在使用 scrapy-redis-bloomfilter 作为去重过滤器，那么每个请求的唯一标识是根据请求的URL生成的哈希值，这个哈希值被用于去重。
            #该方法行不通可能和哈希函数有关
            #random_param = str(random.randint(1, 1000))
            #url_with_param1 = f"{url}?random={random_param}"
            # 第一次访问中间页，解析方法 parse_page
            yield scrapy.Request(
                url=response.urljoin(url),#跳转到第五页
                callback=self.parse_page
            )

        else:
            print("没有找到匹配的URL")

    def parse_page(self, response):
        #self.parse_url_detail(response)
        divs = response.xpath("//div[@class='div_overflow']")
        for div in divs:
            product_url = div.xpath("./a/@href").extract_first()
            yield scrapy.Request(
                url=response.urljoin(product_url),
                callback=self.parse_product_detail,
            )
        page_le = LinkExtractor(restrict_xpaths=("/html/body/div/div[3]/table/tr[64]/td/div/a",))
        page_links = page_le.extract_links(response)
        # print(page_links)
        for page in page_links:
            print(f"有{page.text}页")
            yield scrapy.Request(
                url=response.urljoin(page.url),
                callback=self.parse_url_detail,
                meta={
                    'page':page.text
                }
            )
            print(f"访问第{page.text}页")


    def parse_url_detail(self, response):
        # print(response.text)
        divs = response.xpath("//div[@class='div_overflow']")
        for div in divs:
            product_url = div.xpath("./a/@href").extract_first()
            yield scrapy.Request(
                url=response.urljoin(product_url),
                callback=self.parse_product_detail,
            )
    def parse_product_detail(self, response):

        texts = response.xpath("/html/body/div/div[3]/t/text()").extract()
        # print(texts)
        content = ' '.join(texts)
        # print(content)
        publish_time = response.xpath("//table[@id='label_info']/tr[3]/td[8]/text()").extract_first()
        price = response.xpath("//table[@id='label_info']/tr[3]/td[4]/span/text()").extract_first()
        fetch_time = datetime.datetime.now()
        type = response.xpath("//table[@class='table_user_text']/tr[2]/td/a[2]/text()").extract_first()
        title = response.xpath("//table[@class='table_user_text']/tr[2]/td/a[3]/text()").extract_first()
        url = response.url
        source = "zwaw"
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
