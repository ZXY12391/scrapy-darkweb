
from cnaw.settings import REDIS_HOST,REDIS_DB,REDIS_PARAMS,REDIS_PORT,get_redis_connection
def seekurl():
    redis_conn = get_redis_connection()
    urlCabyc = 'http://cabyceogpsji73sske5nvo45mdrkbz4m3qd3iommf3zaaa6izg3j2cqd.onion/api/category/goods?page_num=1&page_size=10&order=&order_by='
    urlAsap='http://asap4g7boedkl3fxbnf2unnnr6kpxnwoewzw4vakaxiuzfdo5xpmy6ad.onion/'
    urlKingdom = 'http://kingdomm7v6yed55o2rbspvs4exn5bzfxdizqaav27tw6gw4zc65vdad.onion/?t=a006523b031de572'
    urlMgmGrand = 'http://duysanjqxo4svh35yqkxxe5r54z2xc5tjf6r3ichxd3m2rwcgabf44ad.onion/#subscribe-modal'
    urlNemesis = 'http://wvp2anhcslscv7tg3kpbdf2oklhaelhla72l3nkzndubqrjldrjai3id.onion'
    urlTorrez = 'http://mmd32xdcmzrdlpoapkpf43dxig5iufbpkkl76qnijgzadythu55fvkqd.onion/home'
    #urlZwaww='http://mxxxxxxxs4uqwd6cylditj7rh7zaz2clh7ofgik2z5jpeq5ixn4ziayd.onion'
    redis_conn.lpush('search_cabyc', urlCabyc)
    redis_conn.lpush('search_asap', urlAsap)
    redis_conn.lpush('search_kingdom', urlKingdom)
    redis_conn.lpush('search_MgmGrand', urlMgmGrand)
    redis_conn.lpush('search_nemesis', urlNemesis)
    redis_conn.lpush('search_torrez', urlTorrez)
    #redis_conn.lpush('search_zwaww',urlZwaww)
seekurl()
