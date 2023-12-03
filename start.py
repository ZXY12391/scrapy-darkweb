from selenium import webdriver

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--disable-dev-shm-usage')
#chrome_options.binary_location = '/home/chrome-linux64/chrome'

#chrome_driver_path = '/home/chromedriver-linux64/chromedriver'
#service = webdriver.chrome.service.Service(chrome_driver_path)

web=webdriver.Chrome( options=chrome_options)
web.get("https://www.baidu.com")
print(web.page_source)

