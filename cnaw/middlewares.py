from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrapy import signals
from selenium import webdriver
from random import choice
import random
from cnaw.settings import USER_AGENT_LIST
import redis
from cnaw.settings import get_redis_connection
from cnaw.utils.cookie import getCookie
import pymongo
from cnaw.settings import MongoDB
from cnaw.settings import Proxy
from cnaw.settings import REDIS_DB,REDIS_HOST,REDIS_PORT,REDIS_PARAMS
class UAMiddleware:
    def process_request(self, request, spider):
        #设置UA
        ua=choice(USER_AGENT_LIST)
        request.headers["User-Agent"]=ua
        #print(ua)
        return None
    # Add more proxy servers as needed
class ProxyMiddleware:
    def process_request(self, request, spider):
            request.meta['proxy'] = Proxy  # 设置为暗网代理
class BaseMiddleware:
    def __init__(self):
        self.cookie = {}
        self.redis_conn = get_redis_connection()

    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def setup_webdriver(self, spider, url):
        proxy = Proxy
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument(f'--proxy-server={proxy}')
        #chrome_options.add_argument('--headless')
        #chrome_options.add_argument('--disable-gpu')  # 在无头模式下禁用GPU加速
        web = webdriver.Chrome(options=chrome_options)
        web.get(url)
        return web
    def process_request(self, request, spider):
        pass

    def spider_opened(self, spider):
        pass
class LoginMiddleware(BaseMiddleware):
    def login_logic(self, spider, web):
        pass

    def process_request(self, request, spider):
        if spider.name == self.target_spider:
            if not request.cookies:
                request.cookies = self.cookie

    def spider_opened(self, spider):
        if spider.name == self.target_spider:
            self.login_logic(spider)
class LoginZwawwMiddleware(LoginMiddleware):
    target_spider = 'zwaww'
    login_url = "http://mxxxxxxxs4uqwd6cylditj7rh7zaz2clh7ofgik2z5jpeq5ixn4ziayd.onion"
    def login_logic(self, spider):
        cookie_name = 'Zwaw_cookie'
        if self.redis_conn.exists(cookie_name):
            print("Using existing cookie from Redis.")
            self.cookie = self.redis_conn.hgetall(cookie_name)
            return
        web = self.setup_webdriver(spider, self.login_url)
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
        self.redis_conn.hmset(cookie_name, self.cookie)
        print("登录后的URL:", web.current_url)
         #把URL推到Redis队列
        redis_host = REDIS_HOST
        redis_port = REDIS_PORT
        redis_db = REDIS_DB
        redis_password = REDIS_PARAMS.get('password')
        redis_conn = redis.StrictRedis(host=redis_host, password=redis_password, port=redis_port, db=redis_db)
        redis_conn.lpush('search_zwaww', web.current_url)
class LoginNemesisMiddleware(LoginMiddleware):
    target_spider = 'nemesis'
    login_url = "http://wvp2anhcslscv7tg3kpbdf2oklhaelhla72l3nkzndubqrjldrjai3id.onion"
    def login_logic(self, spider):
        cookie_name = 'Nemesis_cookie'
        if self.redis_conn.exists(cookie_name):
            print("Using existing cookie from Redis.")
            self.cookie = self.redis_conn.hgetall(cookie_name)
            return
        web = self.setup_webdriver(spider, self.login_url)
        wait = WebDriverWait(web, 100)  # 最长等待时间为10秒
        # 使用显式等待等待元素可见
        element = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "/html/body/div/nav[2]/div/div/ul/li[2]/a")))
        self.cookie = {item['name']: item['value'] for item in web.get_cookies()}
        print(web.get_cookies())
        # 获取登录后的URL
        print(self.cookie)
        self.redis_conn.hmset(cookie_name, self.cookie)
class LoginAsapMiddleware(LoginMiddleware):
    target_spider = 'asap'
    login_url = "http://asap4g7boedkl3fxbnf2unnnr6kpxnwoewzw4vakaxiuzfdo5xpmy6ad.onion/auth/login"
    def login_logic(self, spider):
        cookie_name='Asap_cookie'
        if self.redis_conn.exists(cookie_name):
            print("Using existing cookie from Redis.")
            self.cookie = self.redis_conn.hgetall(cookie_name)
            return
        web = self.setup_webdriver(spider, self.login_url)
        wait = WebDriverWait(web, 100)  # 最长等待时间为10秒
        # 使用显式等待等待元素可见
        element = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//div[@class='image']")))
        # 刷新页面
        web.refresh()
        element = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//*[@id='Username']")))
        userName1 = "wenyan"
        passwd1 = "asappass"
        web.find_element(by="xpath",
                         value="//*[@id='Username']").send_keys(
            userName1)
        web.find_element(by="xpath",

                         value="//*[@id='Password']").send_keys(
            passwd1)
        img_element = web.find_element(by="xpath", value="//img[@class='card-media-image']")
        # 截取SVG元素并保存为图片
        img_element.screenshot("captchaAsap.png")
        # 等待用户输入验证码
        captcha_input = input("请输入验证码: ")
        web.find_element(by="xpath",
                         value="//*[@id='Captcha']").send_keys(captcha_input)
        web.find_element(by="xpath", value="//button").click()
        web.refresh()
        element = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "/html/body/div/div[2]/nav/section/section[2]/label")))
        self.cookie = {item['name']: item['value'] for item in web.get_cookies()}
        print(web.get_cookies())
        # 获取登录后的URL
        print(self.cookie)
        self.redis_conn.hmset(cookie_name, self.cookie)
class LoginTorrezMiddleware(LoginMiddleware):
    target_spider = 'torrez'
    login_url = "http://mmd32xdcmzrdlpoapkpf43dxig5iufbpkkl76qnijgzadythu55fvkqd.onion"
    def login_logic(self, spider):
        cookie_name = 'Torrez_cookie'
        #if self.redis_conn.exists(cookie_name)and len(self.redis_conn.hgetall(cookie_name)) > 5:
         #   print("Using existing cookie from Redis.")
          #  self.cookie = random.choice(list(self.redis_conn.hvals(cookie_name)))
           # return
        web = self.setup_webdriver(spider, self.login_url)
        wait = WebDriverWait(web, 100)  # 最长等待时间为10秒
        # 使用显式等待等待元素可见
        element = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//img")))
        img_element = web.find_element(by="xpath", value="//img")
        # 截取SVG元素并保存为图片
        img_element.screenshot("captchatorrez1.png")
        # 等待用户输入验证码
        # 等待用户输入验证码
        captcha_input_hour = input("请输入小时: ")
        captcha_input_minute = input("请输入分钟: ")
        # 选择小时
        hour_select = web.find_element(By.XPATH, "//select[@name='h']")
        hour_select.click()
        hour_option = hour_select.find_element(By.XPATH, f"//option[@value='{captcha_input_hour}']")
        hour_option.click()
        # 选择分钟
        minute_select = web.find_element(By.XPATH, "//select[@name='m']")
        minute_select.click()
        minute_option = minute_select.find_element(By.XPATH, f"//option[@value='{captcha_input_minute}']")
        minute_option.click()
        web.find_element(by="xpath", value="//button").click()
        element = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//*[@id='username']")))
        userName1 = "wenyan"
        passwd1 = "torrezpass"
        web.find_element(by="xpath",
                         value="//*[@id='username']").send_keys(
            userName1)
        web.find_element(by="xpath",

                         value="//*[@id='password']").send_keys(
            passwd1)
        img_element = web.find_element(by="xpath", value="//img")
        # 截取SVG元素并保存为图片
        img_element.screenshot("captchatorrez2.png")
        # 等待用户输入验证码
        captcha_input = input("请输入验证码: ")
        web.find_element(by="xpath",
                         value="//*[@id='inputCaptcha']").send_keys(captcha_input)
        web.find_element(By.XPATH, "//button[@type='submit']").click()
        self.cookie = {item['name']: item['value'] for item in web.get_cookies()}
        print(web.get_cookies())
        # 获取登录后的URL
        print(self.cookie)
        self.redis_conn.hmset(cookie_name, self.cookie)
class LoginMGMGrandMiddleware(LoginMiddleware):
    target_spider = 'MGMGrand'
    login_url = "http://duysanjqxo4svh35yqkxxe5r54z2xc5tjf6r3ichxd3m2rwcgabf44ad.onion/signin"
    def login_logic(self, spider):
        cookie_name = 'MGMGrand_cookie'
        if self.redis_conn.exists(cookie_name):
            print("Using existing cookie from Redis.")
            self.cookie = self.redis_conn.hgetall(cookie_name)
            return
        web = self.setup_webdriver(spider, self.login_url)
        wait = WebDriverWait(web, 100)  # 最长等待时间为10秒
        # 使用显式等待等待元素可见
        with open("page.html", "w", encoding="utf-8") as file:
            file.write(web.page_source)
        element = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@id='username']")))
        userName1 = "wenyanMGM"
        passwd1 = "mgmpassword"
        web.find_element(by="xpath",
                         value="//input[@id='username']").send_keys(
            userName1)

        web.find_element(by="xpath",

                         value="//*[@id='password']").send_keys(
            passwd1)
        img_element = web.find_element(by="xpath", value="//img[@class='img-recaptcha']")
        # 截取SVG元素并保存为图片
        img_element.screenshot("captchaMGM.png")
        # 等待用户输入验证码
        captcha_input = input("请输入验证码: ")
        web.find_element(by="xpath",
                         value="//*[@id='recaptcha']").send_keys(captcha_input)
        web.find_element(by="xpath", value="//button").click()

        self.cookie = {item['name']: item['value'] for item in web.get_cookies()}
        print(web.get_cookies())
        # 获取登录后的URL
        print(self.cookie)
        self.redis_conn.hmset(cookie_name, self.cookie)
class LoginCabycMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.
    def __init__(self):
        #登陆后获得的
        self.Authorization=getCookie('cookie_cabyc')
        print(self.Authorization)
    def process_request(self, request, spider):
        if spider.name == 'cabyc':
            request.headers['Authorization'] = self.Authorization

class LoginKingdomMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.
        def __init__(self):
            # 登陆后获得的 Cookie 字符串
            cookie_string = getCookie('cookie_kingdom')
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
                request.cookies = getCookie('cookie_kingdom')
