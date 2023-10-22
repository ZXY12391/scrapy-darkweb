import scrapy
import os
import datetime
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from cnaw.items import CnawItem


class ZwawSpider(CrawlSpider):
    name = "zwaw"
    start_urls = [
        "http://mxxxxxxxs4uqwd6cylditj7rh7zaz2clh7ofgik2z5jpeq5ixn4ziayd.onion/index.php?parameter=946cgt1Ix6JHWjEw8WrfgK9htbsnQbmUnSaQ9itMgK7YwUEwWtE1iIGuTv2aCpJknt8PmBnZnEfLEAraNnN3GaIU3k1HNYPpH9dOAZdMZiPK1aU0ScyLj4YFvXOUITbwUFnSNFiKRjqejfe-SfA69Sti8wr_eo1A3EH9arY"]

    def start_requests(self):
            url = self.read_url_from_file()
            yield scrapy.Request(url, callback=self.parse)
    def read_url_from_file(self):
            url = None
            file_path = "cnaw/logged_in_url.txt"
            with open(file_path, "r") as file:
                url = file.read().strip()
            # 清除文件内容
            with open(file_path, "w") as file:
                file.truncate(0)
            return url

    def parse(self, response):
        print(response.text)
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

    def parse_by1(self, response):  # 按照发布时间
        # 发布时间链接
        href = response.xpath("/html/body/div/div[3]/table/tr[1]/td/a[1]/@href").extract_first()
        yield scrapy.Request(
            url=href,
            callback=self.parse_url_detail,  # 解析方法需要改变,回调函数
        )

    def parse_url_detail(self, response):
        # print(response.text)
        divs = response.xpath("//div[@class='div_overflow']")
        for div in divs:
            product_url = div.xpath("./a/@href").extract_first()
            # title=div.xpath("./a/text()").extract_first()
            # print(title)
            yield scrapy.Request(
                url=product_url,
                callback=self.parse_product_detail,
            )
        # 翻页
        page_le = LinkExtractor(restrict_xpaths=("/html/body/div/div[3]/table/tr[64]/td/div/a",))
        page_links = page_le.extract_links(response)
        # print(page_links)
        for page in page_links:
            # print(page.url)
            yield scrapy.Request(
                url=page.url,  # 有重复的URL没关系，scrapy会帮我们自动去重
                callback=self.parse_url_detail  # 循环上述操作
            )

    def parse_product_detail(self, response):
        print(f"第{self.num2}{response.url}")
        self.num2 = self.num2 + 1
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
