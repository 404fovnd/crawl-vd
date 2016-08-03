from scrapy.contrib.downloadermiddleware.useragent import UserAgentMiddleware

class tutUseragent(UserAgentMiddleware):
    def __init__(self, user_agent = ''):
        self.user_agent = user_agent

    def process_request(self, request, spider):
        ua = 'Mozilla/5.0 (X11; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0'
        request.headers.setdefault('User-Agent', ua)
