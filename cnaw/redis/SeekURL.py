import pymongo
from cnaw.settings import MongoDB
from cnaw.settings import get_redis_connection

def ConnectMongo():
    client = pymongo.MongoClient(host=MongoDB['host'], port=MongoDB['port'])
    db = client['local']
    # db.authenticate("local","123456")
    collection = db['StartURL']
    return collection

def insert_urls_to_mongodb(collection):
    urls = {
        'search_cabyc': 'http://cabyceogpsji73sske5nvo45mdrkbz4m3qd3iommf3zaaa6izg3j2cqd.onion/api/category/goods?cid=1&page_num=1&page_size=10&order=&order_by=',
        'search_asap': 'http://asap4g7boedkl3fxbnf2unnnr6kpxnwoewzw4vakaxiuzfdo5xpmy6ad.onion/',
        'search_kingdom': 'http://kingdomm7v6yed55o2rbspvs4exn5bzfxdizqaav27tw6gw4zc65vdad.onion/?t=a006523b031de572',
        'search_MgmGrand': 'http://duysanjqxo4svh35yqkxxe5r54z2xc5tjf6r3ichxd3m2rwcgabf44ad.onion/#subscribe-modal',
        'search_nemesis': 'http://wvp2anhcslscv7tg3kpbdf2oklhaelhla72l3nkzndubqrjldrjai3id.onion',
        'search_torrez': 'http://mmd32xdcmzrdlpoapkpf43dxig5iufbpkkl76qnijgzadythu55fvkqd.onion/home',
        #'search_zwaww': 'http://mxxxxxxxsjznlccmh5p64nambxuoklg44kmjscl2nkvgoolnzeiqbmqd.onion',
        'search_freecity': 'http://xbtppbb7oz5j2stohmxzvkprpqw5dwmhhhdo2ygv6c7cs4u46ysufjyd.onion/market'
    }
    for key, url in urls.items():
        collection.insert_one({'name': key, 'url': url})


def main():
    collection = ConnectMongo()
    insert_urls_to_mongodb(collection)

if __name__ == "__main__":
    main()
