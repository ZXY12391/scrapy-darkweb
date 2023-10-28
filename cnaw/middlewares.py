# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrapy import signals
from selenium import webdriver
import ddddocr
import base64
# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
import time
from selenium.webdriver import Chrome
from selenium.webdriver import Firefox
from random import choice
from cnaw.settings import USER_AGENT_LIST
import redis
from scrapy_redis.spiders import RedisSpider  # 导入 RedisSpider
from cnaw.settings import REDIS_DB,REDIS_HOST,REDIS_PORT,REDIS_PARAMS
class ProxyMiddleware:
    def process_request(self, request, spider):
            request.meta['proxy'] = "http://127.0.0.1:8118"  # 设置为暗网代理
class Login2Middleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.
    def __init__(self):
        #登陆后获得的

        self.Authorization="Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHBpcmUiOjE2OTg0ODg1MzYsImhpZCI6IjMzNzc3NTc1OSIsImxldmVsIjowfQ.okcek9cuOI37HguVdToGmSTrNMVYTS4PI0ZvSIO2j6k"
    def process_request(self, request, spider):
        if spider.name == 'cabyc':
            request.headers['Authorization'] = self.Authorization
class Login1Middleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.
        def __init__(self):
            # 登陆后获得的 Cookie 字符串
            cookie_string = "PHPSESSID=nc9k4omocc3ogbjtqe05g0q8r6; uuid=1896236"
            #print("zzzzz")

            # 将 Cookie 字符串分割成键值对
            cookie_pairs = cookie_string.split('; ')
            #print(cookie_pairs)
            # 创建一个字典来存储 Cookie 键值对
            self.cookie = {}
            for pair in cookie_pairs:
                key, value = pair.strip().split('=')
                self.cookie[key] = value
           #print(self.cookie)

        def process_request(self, request, spider):
            if spider.name == 'zwaw':
                request.cookies = self.cookie
            #print(request.cookies)

class Login4Middleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.
        def __init__(self):
            # 登陆后获得的 Cookie 字符串
                cookie_string = "PHPSESSID=0riq2kbugjo3c7scd65ocnrs2i; pc_333f7gpuishjximodvynnoisxujicgwaetzywgkxoxuje5ph3qyqjuid_onion__XSRF-TOKEN=eyJpdiI6IkFlUmV0NUdieHRNbWV0cEhwb0VZd0E9PSIsInZhbHVlIjoidW5VZzV4cnhFU2xJYVwvVXZwYmZIc3Q1RWZORTNqZWJncDZQTUpPZkgzc1F2aExqU1laVmdaWVJhYllyMnJtMzZlZUlrYmVOY3g2NFR3MG54ZzJ6eTZlaUlOXC91cCtENkoyXC9nZ0FTd1B1VURCNDkzaFY5Q3BFZkVuRHZFSnFlY0giLCJtYWMiOiJlOWRhM2FjNTRkYjNkYTA1YjIxYzdmMzRkNGNmOGE1ZWY4OTFjMTNhYjkxN2JkYzk2YWVmY2ZmOGM5ZjQ3NWZlIn0%3D; pc_333f7gpuishjximodvynnoisxujicgwaetzywgkxoxuje5ph3qyqjuid_onion__hr4ujvby8ds459og4kzcpbzwjdj_session=eyJpdiI6InlhazVNQzdVRmlRTFwvTnoyN1wvNEIxQT09IiwidmFsdWUiOiJSaU12Z1J0b2xSTjlNaittY0pSMEY2N1pEN1g1eXdKb1NQeU9DalRpaUY2cW43a0owQ1c2XC9SRm5HT3BCU1VLOStuOVhwRkNrOHltY3NoRkxZaWdBdE81b0lzbFM2K0xVeTBCcjlCYzR5WFYzblBTeGgxa1VzejdYandQWHZMWHYiLCJtYWMiOiJiNTBmNzNmZjMyMDJiZjA3NDYwYTA3NzkzZjNiMzQxMGY2MzRiNmFkOWM4NmE1NzE2ZDQ1ZjVkYWNiZjg0Yzk4In0%3D"
                # 将 Cookie 字符串分割成键值对
                cookie_pairs = cookie_string.split('; ')
                #print(cookie_pairs)
                # 创建一个字典来存储 Cookie 键值对
                self.cookie = {}
                for pair in cookie_pairs:
                    key, value = pair.strip().split('=')
                    self.cookie[key] = value
                #print(self.cookie)
        def process_request(self, request, spider):
            if spider.name == 'torrez':
                request.cookies = self.cookie
                print(request.cookies)
class UAMiddleware:

    def process_request(self, request, spider):
        #设置UA
        ua=choice(USER_AGENT_LIST)
        request.headers["User-Agent"]=ua
        #print(ua)
        return None

    # Add more proxy servers as needed
class Login3Middleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.
    def __init__(self):
        self.cookie = {}  # 初始化cookie为空字典

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.

        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        if spider.name == 'zwaww':
            if not request.cookies:  # 简单判断是否有cookie，没有的话就设置一下
                request.cookies = self.cookie
                print(request.cookies)
            return None

    def spider_opened(self, spider):
        # 配置代理
        if spider.name == 'zwaww':
            proxy = "http://127.0.0.1:8118"
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument(f'--proxy-server={proxy}')
            # 启动Chrome浏览器
            web = webdriver.Chrome(options=chrome_options)
            web.get(
                "http://mxxxxxxxs4uqwd6cylditj7rh7zaz2clh7ofgik2z5jpeq5ixn4ziayd.onion")

            wait = WebDriverWait(web, 40)  # 最长等待时间为10秒
            # 使用显式等待等待元素可见
            element = wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, "/html/body/div/div[1]/div/a/span")))
            web.find_element(by="xpath", value="/html/body/div/div[1]/div/a/span").click()
            element = wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, "/html/body/div/div[3]/div[1]/a[1]")))
            web.find_element(by="xpath", value="/html/body/div/div[3]/div[1]/a[1]").click()
            # 使用显式等待等待元素可见
            element = wait.until(EC.visibility_of_element_located(
                (By.XPATH, "/html/body/div/div[3]/form/fieldset/input[1]")))
            userName1 = "1896236"
            passwd1 = "1234awxmhh"
            web.find_element(by="xpath",
                             value="/html/body/div/div[3]/form/fieldset/input[1]").send_keys(
                userName1)
            web.find_element(by="xpath",
                             value="/html/body/div/div[3]/form/fieldset/input[2]").click()
            element = wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, "/html/body/div/div[3]/form/fieldset/input[1]")))
            web.find_element(by="xpath",
                             value="/html/body/div/div[3]/form/fieldset/input[1]").send_keys(
                passwd1)
            web.find_element(by="xpath",
                             value="/html/body/div/div[3]/form/fieldset/input[2]").click()
            element = wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, "/html/body/div/div[2]/form/fieldset/input[1]")))
            # print(web.page_source)
            web.find_element(by="xpath",
                             value="/html/body/div/div[2]/form/fieldset/input[1]").send_keys(
                passwd1)
            web.find_element(by="xpath",
                             value="/html/body/div/div[2]/form/fieldset/input[2]").click()
            self.cookie = {item['name']: item['value'] for item in web.get_cookies()}
            print(web.get_cookies())
            # 获取登录后的URL
            print(self.cookie)
            with open("cnaw/logged_in_url.txt", "w") as file:
                file.write(web.current_url)
            print("登录后的URL:", web.current_url)
            #把URL推到Redis队列
            redis_host = REDIS_HOST
            redis_port = REDIS_PORT
            redis_db = REDIS_DB
            redis_password = REDIS_PARAMS.get('password')
            redis_conn = redis.StrictRedis(host=redis_host, password=redis_password, port=redis_port, db=redis_db)
            redis_conn.lpush('search_url', web.current_url)

class Login6Middleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.
    def __init__(self):
        self.cookie = {}  # 初始化cookie为空字典

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.

        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        if spider.name == 'freeforum':
            if not request.cookies:  # 简单判断是否有cookie，没有的话就设置一下
                request.cookies = self.cookie
                print(request.cookies)
            return None

    def spider_opened(self, spider):
        # 配置代理
        if spider.name == 'freeforum':
            proxy = "http://127.0.0.1:8118"
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument(f'--proxy-server={proxy}')
            # 启动Chrome浏览器
            web = webdriver.Chrome(options=chrome_options)
            web.get(
                "http://freedxxxrbrtxigoiyf333cradalwequhwocpv5wime7cxkrsk2bidqd.onion/index.php?m=u&c=login")

            wait = WebDriverWait(web, 100)  # 最长等待时间为10秒
            # 使用显式等待等待元素可见

            element = wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//*[@id='J_u_login_username']")))
            userName1 = "wenyan"
            passwd1 = "freecitypass"
            web.find_element(by="xpath",
                             value="//*[@id='J_u_login_username']").send_keys(
                userName1)
            web.find_element(by="xpath",

                             value="//*[@id='J_u_login_password']").send_keys(
                passwd1)
            web.find_element(by="xpath", value="/html/body/div/div[3]/div/div[1]/div/form/div/dl[4]/dd/button").click()
            element = wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//h3[@class='fname'][1]/a")))
            web.find_element(by="xpath", value="//h3[@class='fname'][1]/a").click()

            self.cookie = {item['name']: item['value'] for item in web.get_cookies()}
            print(web.get_cookies())
            # 获取登录后的URL
            print(self.cookie)
class Login7Middleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.
    def __init__(self):
        self.cookie = {}  # 初始化cookie为空字典

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.

        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        if spider.name == 'nemesis':
            if not request.cookies:  # 简单判断是否有cookie，没有的话就设置一下
                request.cookies = self.cookie
                print(request.cookies)
            return None

    def spider_opened(self, spider):
        # 配置代理
        if spider.name == 'nemesis':
            proxy = "http://127.0.0.1:8118"
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument(f'--proxy-server={proxy}')
            # 启动Chrome浏览器
            web = webdriver.Chrome(options=chrome_options)
            web.get(
                "http://wvp2anhcslscv7tg3kpbdf2oklhaelhla72l3nkzndubqrjldrjai3id.onion")

            wait = WebDriverWait(web, 100)  # 最长等待时间为10秒
            # 使用显式等待等待元素可见

            element = wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, "/html/body/div/nav[2]/div/div/ul/li[2]/a")))
            self.cookie = {item['name']: item['value'] for item in web.get_cookies()}
            print(web.get_cookies())
            # 获取登录后的URL
            print(self.cookie)

class Login8Middleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.
        def __init__(self):
            # 登陆后获得的 Cookie 字符串
            cookie_string = "PHPSESSID=9cm9vi2o2lnhl22no9hv1fahso"
            # 将 Cookie 字符串分割成键值对
            cookie_pairs = cookie_string.split('; ')
            #print(cookie_pairs)
            # 创建一个字典来存储 Cookie 键值对
            self.cookie = {}
            for pair in cookie_pairs:
                key, value = pair.strip().split('=')
                self.cookie[key] = value
            #print(self.cookie)
        def process_request(self, request, spider):
            if spider.name == 'asap':
                request.cookies = self.cookie
                print(request.cookies)
class Login9Middleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.
        def __init__(self):
            # 登陆后获得的 Cookie 字符串
            cookie_string = "PHPSESSID=45logbg3ahponp530dhaf88umo"
            # 将 Cookie 字符串分割成键值对
            cookie_pairs = cookie_string.split('; ')
            #print(cookie_pairs)
            # 创建一个字典来存储 Cookie 键值对
            self.cookie = {}
            for pair in cookie_pairs:
                key, value = pair.strip().split('=')
                self.cookie[key] = value
            print(self.cookie)
        def process_request(self, request, spider):
            if spider.name == 'kingdom':
                request.cookies = self.cookie