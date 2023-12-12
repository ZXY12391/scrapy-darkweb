import sys
sys.path.append(r"C:\Users\26347\Desktop\pythonProject\cnaw")
import pymongo
from cnaw.settings  import MongoDB
from datetime import datetime
import pymongo

def getLatestTime(Website):
    client = pymongo.MongoClient(host=MongoDB['host'], port=MongoDB['port'])
    db = client['DW']
    collection = db[Website]

    # Sort by timestamp field in descending order and retrieve the first document
    latest_record = collection.find_one(sort=[('Publish_time', pymongo.DESCENDING)])

    if latest_record:
        latest_Time = latest_record['Publish_time']
        return latest_Time
    else:
        return None  # Handle case where collection is empty or no timestamp field exists

def check_existence(url,Website):
    client = pymongo.MongoClient(host=MongoDB['host'], port=MongoDB['port'])
    db = client['DW']
    collection = db[Website]

    # 构建查询条件
    query = {'Url': url}

    # 在集合中查询是否存在相同内容的数据
    result = collection.find_one(query)

    if result:
        # 如果存在相同内容的数据
        #print("存在相同内容的数据：", result)
        return True
    else:
        # 如果不存在相同内容的数据
        #print("不存在相同内容的数据")
        return False
#print(getLatestTime('Zwaw'))
url="http://mmd32xdcmzrdlpoapkpf43dxig5iufbpkkl76qnijgzadythu55fvkqd.onion/items/ps5-bot-100-working-2020-exlusive-bot"
Website='Torrez'
result=check_existence(url,Website)
print(result)
if result:
    print("1")