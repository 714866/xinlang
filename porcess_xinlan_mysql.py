#encoding=utf-8
import redis
import MySQLdb
from xinlannews.settings import MYSQL_HOST
from xinlannews.settings import MYSQL_PORT
from xinlannews.settings import MYSQL_USER
from xinlannews.settings import MYSQL_PASSWD
from xinlannews.settings import REDIS_HOST
from xinlannews.settings import REDIS_PORT
import json
import sys
import time
reload(sys)
sys.setdefaultencoding('utf8')

def process():
    redisCli = redis.Redis(host=REDIS_HOST,port=int(REDIS_PORT))
    info = 0

    while info<10:

        try:
            source, data = redisCli.blpop('newspider:items')
            item = json.loads(data)
            print item

            mysqlCli = MySQLdb.connect(host=MYSQL_HOST, port=int(MYSQL_PORT), user=MYSQL_USER,passwd=MYSQL_PASSWD, db='xinlan',charset='utf8')
            cur = mysqlCli.cursor()
            if len(item['parentUrl'])==0:
                cur.execute(
                    'INSERT INTO detial (parentUrl, parentTitle, subTitle, subUrl, subFilenamae, articleUrl, content, article)'
                    ' VALUES ( %s , %s,%s, %s, %s, %s, %s,%s);',
                    ['NULL',str(item["parentTitle"][0]).encode('utf-8'),
                     str(item["subTitle"]).encode('utf-8'),str(item["subUrl"]).encode('utf-8'),
                     str(item["subFilename"]).encode('utf-8'),str(item["article"]).encode('utf-8'),
                     str(item["content"]).encode('utf-8'),str(item["article"]).encode('utf-8')
                     ]
                )
            else:
                cur.execute(
                    'INSERT INTO detial (parentUrl, parentTitle, subTitle, subUrl, subFilenamae, articleUrl, content, article)'
                    ' VALUES ( %s , %s,%s, %s, %s, %s, %s,%s);',
                    [str(item['parentUrl'][0].encode("utf-8")), str(item["parentTitle"][0]).encode('utf-8'),
                     str(item["subTitle"]).encode('utf-8'), str(item["subUrl"]).encode('utf-8'),
                     str(item["subFilename"]).encode('utf-8'), str(item["article"]).encode('utf-8'),
                     str(item["content"]).encode('utf-8'), str(item["article"]).encode('utf-8')
                     ]
                )

            mysqlCli.commit()
            cur.close()
            info+=1
        except:
            time.sleep(10)
            redisCli.blpush('newspider:items',item)
            print 'xxx'

def main():
    process()
    print '完成'

    pass

if __name__=='__main__':
    process()
