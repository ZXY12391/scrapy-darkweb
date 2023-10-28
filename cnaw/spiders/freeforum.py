import scrapy
from cnaw.items import CnawItem
import datetime
from scrapy_redis.spiders import RedisSpider  # 导入 RedisSpider
from cnaw.settings import REDIS_HOST,REDIS_DB,REDIS_PARAMS,REDIS_PORT
from scrapy.linkextractors import LinkExtractor
import redis
class FreeforumSpider(RedisSpider):
    name = "freeforum"
    redis_key = "search_url"
    start_urls = ["http://freedxxxrbrtxigoiyf333cradalwequhwocpv5wime7cxkrsk2bidqd.onion/index.php?c=thread&fid=46"]
    def __init__(self, *args, **kwargs):
        super(FreeforumSpider, self).__init__(*args, **kwargs)
        url = 'http://freedxxxrbrtxigoiyf333cradalwequhwocpv5wime7cxkrsk2bidqd.onion/index.php?c=thread&fid=46'
        # 请替换为您自己的Redis连接信息
        redis_host = REDIS_HOST
        redis_port = REDIS_PORT
        redis_db = REDIS_DB
        redis_password = REDIS_PARAMS.get('password')
        redis_conn = redis.StrictRedis(host=redis_host, password=redis_password, port=redis_port, db=redis_db)
        redis_conn.lpush('search_url', url)
    def parse(self, response):
        #print(response.text)
        tds=response.xpath("//div[@class='thread_posts_list']/table/tr/td[1]")
        for td in tds:
            href=td.xpath("./p/a[@class='st']/@href").extract_first()
            print(href)
            if href:
                yield scrapy.Request(
                    url=response.urljoin(href),
                    callback=self.parse_detail,
                )
        #翻页
        page_le = LinkExtractor(restrict_xpaths=("//div[@class='pages']/a",))
        page_links = page_le.extract_links(response)
        for page in page_links:
                yield scrapy.Request(
                    url=response.urljoin(page.url),
                     callback=self.parse,
                    )

    def parse_detail(self,response):
        title=response.xpath("//h1[@id='J_post_title']/text()").extract_first()
        type=response.xpath("//h1[@id='J_post_title']/a/text()").extract_first()
        text_content=response.xpath("//div[@class='editor_content']//text()").extract()
        content = ' '.join(text_content)
        publish=response.xpath("/html/body/div/div[3]/div[5]/div[2]/table/tr[1]/td[2]/div[4]/span/text()").extract_first()#还要处理
        fetch_time = datetime.datetime.now()
        source='freeforum'
        url=response.url
        price=None
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





