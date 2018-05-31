# _*_ encoding=utf-8  _*_
from xinlannews.settings import MONGODB_HOST
from xinlannews.settings import MONGODB_PORT
from xinlannews.settings import REDIS_HOST
from xinlannews.settings import REDIS_PORT
import redis
import pymongo
import json

def main():
    #创建mongodb连接
    mongoClient = pymongo.MongoClient(host=MONGODB_HOST,port=int(MONGODB_PORT))
    #创建redis连接
    redisClient = redis.StrictRedis(host=REDIS_HOST,port=int(REDIS_PORT),db=0)

    #mongodb的库，如mongodb没有这个库，则创建这个库，
    db = mongoClient['xinlang']
    #连接到表
    sheet = db['news']

    while True:
        source, data = redisClient.blpop(['newspider:items'])

        item = json.loads(data)
        sheet.insert(item)
    print('ok')

if __name__=='__main__':
    main()
