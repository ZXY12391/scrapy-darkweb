import pymongo
from cnaw.settings import MongoDB
from datetime import datetime
import random
def ConnectMongo():
    client = pymongo.MongoClient(host=MongoDB['host'], port=MongoDB['port'])
    db = client['local']
    # db.authenticate("local","123456")
    collection = db['Cookie']
    return collection


def insert_Cookies_to_mongodb(collection):
    cookies = {
        # 长安不夜城用户名：wenyancabyc密码：Cabycpass1*
        'cookie_cabyc': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHBpcmUiOjE3MDA4MTM3OTksImhpZCI6IjEzMDMxNDI1ODYiLCJsZXZlbCI6MH0.GIduxu1CQDkfcn-twz3sswWcSjLX_bKnDkZ1aPYXKoI',
        'cookie_kingdom': [
            'PHPSESSID=91pdeje2t0jca15q5k6bksc6jd',
            'PHPSESSID=vssettjids57srec7o3un6vk20',
            'PHPSESSID=bsir25jfrv8c83lfjc39k1kfkf',
            'PHPSESSID=gb20auvnthck8hqtlmp5e3ior8',
        ],
        # Add more cookies here if needed
    }

    # 删除整个 Cookie 集合中的所有记录
    collection.delete_many({})

    # 插入新的 cookie 记录
    for key, cookie in cookies.items():
        current_time = datetime.now()  # 获取当前时间
        collection.insert_one({'name': key, 'cookie': cookie, 'timestamp': current_time})


def getCookie(cookieName):
    client = pymongo.MongoClient(host=MongoDB['host'], port=MongoDB['port'])
    db = client['local']
    collection = db['Cookie']


    cookies = collection.find({'name': cookieName}, {'cookie': 1, '_id': 0})
    cookies = list(cookies)
    print(cookies)

    # 随机选择一个最新的 cookie
    if cookies:
        cookie_values = cookies[0]['cookie']  # 获取 'cookie' 键对应的值，即列表
        #random_cookie = random.choice(cookie_values)  # 从列表中选择一个值
        #print(random_cookie)
        #return random_cookie
        return cookie_values
    else:
        return None


def main():
    collection = ConnectMongo()
    insert_Cookies_to_mongodb(collection)
    #cookie=getCookie('cookie_kingdom')
    #print(cookie)
if __name__ == "__main__":
    main()
    # cookies_list = []  # 初始化一个空列表用于存储多个字典形式的Cookie
    # cookies = getCookie('cookie_kingdom')
    # for cookie in cookies:
    #     cookie_dict = {}  # 创建一个字典用于存储键值对
    #     cookie_pairs = cookie.split('; ')
    #     for pair in cookie_pairs:
    #         key, value = pair.strip().split('=')
    #         cookie_dict[key] = value
    #     cookies_list.append(cookie_dict)  # 将每个字典添加到列表中
    # random_cookie = random.choice(cookies_list)
    # print(random_cookie)
