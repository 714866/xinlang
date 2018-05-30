import random
from settings import USER_AGENTS
import base64

class RandomUserAgent(object):
    def process_request(self, request, spider):
        user_agent = random.choice (USER_AGENTS)
        request.headers.setdefault('User-Agent',user_agent)

class RandomProxy(object):
    def Proxy(self,request,spider):
        ip = [
            {'ip_port': '111.8.60.9:8123', 'user_passwd': 'user1:pass1'},
            {'ip_port': '101.71.27.120:80', 'user_passwd': 'user2:pass2'},
            {'ip_port': '122.96.59.104:80', 'user_passwd': 'user3:pass3'},
            {'ip_port': '122.224.249.122:8088', 'user_passwd': 'user4:pass4'},
        ]
        proxy = random.choice(ip)

        if proxy['user_passwd'] is None:
            request.meta['proxy'] = 'http://'+proxy['ip_port']
        else:
            u_p = base64.b64encode(proxy['user_passwd'])
            request.headers['Proxy-Authorization']='Basic'+u_p
            request.meta['proxy'] = 'http://'+proxy['ip_port']

