import sys
sys.path.append(r"C:\Users\26347\Desktop\pythonProject\cnaw")
import pymongo
from cnaw.settings import MongoDB
from datetime import datetime

def ConnectMongo(name):
    client = pymongo.MongoClient(host=MongoDB['host'], port=MongoDB['port'])
    db = client['DW']
    # db.authenticate("local","123456")
    collection = db[name]
    return collection
def remove_duplicate_documents(collection):
    # 查找重复数据
    pipeline = [
        {
            '$group': {
                '_id': {'Url': '$Url'},  # 根据字段来判断重复
                'uniqueIds': {'$addToSet': '$_id'},  # 将重复的文档放入数组
                'count': {'$sum': 1}  # 统计重复文档数量
            }
        },
        {
            '$match': {
                'count': {'$gt': 1}  # 找出重复的文档
            }
        }
    ]

    duplicate_docs = list(collection.aggregate(pipeline))

    # 删除重复数据
    for doc in duplicate_docs:
        for id_to_delete in doc['uniqueIds'][1:]:  # 保留一个文档 ID
            collection.delete_one({'_id': id_to_delete})
def get_data_count_by_date_range(start_date, end_date, collection):

    # 查询特定日期范围内的数据数量
    query = {
        'Fetch_time': {
            '$gte': start_date,
            '$lte': end_date
        }
    }

    count = collection.count_documents(query)
    return count






collection = ConnectMongo('Cabyc')  # 替换为你的集合名
remove_duplicate_documents(collection)
# 调用方法并获取数据数量
start_date = datetime(2023, 12, 18, 0, 0, 0)  # 替换为你的开始日期和时间
end_date = datetime(2023, 12, 19, 23, 59, 59)  # 替换为你的结束日期和时间
data_count = get_data_count_by_date_range(start_date, end_date, collection)  # 替换为你的集合名

print(f"从 {start_date} 到 {end_date} 之间的抓取数据数量为: {data_count}")