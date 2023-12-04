import sys
sys.path.append(r"C:\Users\26347\Desktop\pythonProject\cnaw")
from cnaw.settings import get_redis_connection
import pymongo
from cnaw.settings import MongoDB
def ConnectMongo():
    client = pymongo.MongoClient(host=MongoDB['host'], port=MongoDB['port'])
    db = client['DW']
    collection = db['StartURL']
    return collection

def Pushurl():
    redis_conn = get_redis_connection()
    collection = ConnectMongo()
    # 清空整个 Redis 数据库
    redis_conn.flushdb()
    # 获取 MongoDB 中的 URL 数据
    urls = collection.find({}, {'_id': 0, 'name': 1, 'url': 1})
    # 将每个 URL 推送到相应的 Redis 队列中
    for url_data in urls:
        name = url_data['name']
        url = url_data['url']
        redis_conn.lpush(name, url)
        print(name)
Pushurl()
