import scrapy
import datetime
from cnaw.items import CnawItem
from scrapy_redis.spiders import RedisSpider  # 导入 RedisSpider
from cnaw.settings import REDIS_HOST,REDIS_DB,REDIS_PARAMS,REDIS_PORT,get_redis_connection
import redis
class CabycSpider(RedisSpider):
    name = 'cabyc'
    redis_key = "search_cabyc"
    goodDetailBase = "http://cabyceogpsji73sske5nvo45mdrkbz4m3qd3iommf3zaaa6izg3j2cqd.onion/api/goods/detail?gid="
    goodUrlBase="http://cabyceogpsji73sske5nvo45mdrkbz4m3qd3iommf3zaaa6izg3j2cqd.onion/#/detail?gid="

    def parse(self, response):
        # 使用 JSON 解析响应内容
        json_response = response.json()
        #翻页
        total=json_response.get('data', {}).get('total', 0)
        page_size=json_response.get('data',{}).get('page_size',0)
        pages = total // page_size if total % page_size == 0 else (total // page_size) + 1
        print(total)
        print(page_size)
        print(pages)
        for page in range(1,pages+1):
            url=f"http://cabyceogpsji73sske5nvo45mdrkbz4m3qd3iommf3zaaa6izg3j2cqd.onion/api/category/goods?page_num={page}&page_size=10&order=&order_by="
            yield scrapy.Request(
                url=url,
                callback=self.parse_url,

            )
    def parse_url(self,response):
        json_response = response.json()
        #print(json_response)
        # 提取所需的数据
        goods = json_response.get('data', {}).get('goods', [])
        for good in goods:
            gid = good.get('id', '')

            gid = gid[0] if isinstance(gid, tuple) else gid
            gid = str(gid)  # 把元组变为字符串
            #print(self.goodDetailBase + gid)
            yield scrapy.Request(
                url=self.goodDetailBase + gid,
                callback=self.parse_good_detail,

            )
    def parse_good_detail(self, response):
        json_response = response.json()
        #print(json_response)
        if json_response['code'] == 2000:  # 检查JSON中的code字段是否为2000，以确保响应成功
            data = json_response['data']
            Title = data['name']  # 获取商品名称
            Price = data['price']  # 获取商品价格
            Content=data['intro']
            Source="Cabyc"
            Fetch_time = datetime.datetime.now()
            timestamp=data['ctime']
            Publish_time = datetime.datetime.fromtimestamp(timestamp)
            url=self.goodUrlBase+data['id']
            Cid=data['cid']
            if Cid == 1:
                Type = '数据资源'
            elif Cid == 2:
                Type = '服务业务'
            elif Cid == 3:
                Type = '虚拟物品'
            elif Cid == 4:
                Type = '私人专拍'
            elif Cid == 5:
                Type = '卡料CVV'
            elif Cid == 6:
                Type = '影视音像'
            elif Cid == 7:
                Type = '其它类别'
            elif Cid == 8:
                Type = '技术技能'
            elif Cid == 9:
                Type = '实体物品'
            else:
                Type = '未知'  # 如果 cid 不匹配任何已知情况，可以设置一个默认值
            item = CnawItem()
            item['Source'] = Source
            item['Type'] = Type
            item['Title'] = Title
            item['Content'] = Content
            item['Price'] = Price
            item['Publish_time'] = Publish_time
            item['Fetch_time'] = Fetch_time
            item['Url'] = url
            yield item

        else:
            print("JSON响应失败")

