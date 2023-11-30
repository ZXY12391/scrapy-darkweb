import pymongo
from cnaw.settings import MongoDB
from datetime import datetime
def ConnectMongo():
    client = pymongo.MongoClient(host=MongoDB['host'], port=MongoDB['port'])
    db = client['local']
    # db.authenticate("local","123456")
    collection = db['Cookie']
    return collection

def insert_Cookies_to_mongodb(collection):
    cookies = {
        # 长安不夜城用户名：wenyancabyc密码：Cabycpass1*
        'cookie_cabyc': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHBpcmUiOjE3MDEzMjQ5MjEsImhpZCI6IjMzNzc3NTc1OSIsImxldmVsIjowfQ.0NS5GVUGvRzBUbhJA3cyFk7eJGuSUpj-Lte8YtAPGXI',
        'cookie_kingdom': 'PHPSESSID=b254j4fu5se0q6f61f23jdf54q',
    }
    for key, cookie in cookies.items():
        current_time = datetime.now()  # 获取当前时间
        collection.insert_one({'name': key, 'cookie': cookie, 'timestamp': current_time})
def getCookie(cookieName):
    client = pymongo.MongoClient(host=MongoDB['host'], port=MongoDB['port'])
    db = client['local']
    collection = db['Cookie']

    # 按时间戳倒序排序，选择最新的记录
    latest_cookie = collection.find({'name': cookieName}, {'cookie': 1, '_id': 0}).sort('timestamp', -1).limit(1)

    for c in latest_cookie:
        print(c['cookie'])
        return c['cookie']

def main():
    collection = ConnectMongo()
    insert_Cookies_to_mongodb(collection)
    getCookie('cookie_cabyc')

if __name__ == "__main__":
    main()