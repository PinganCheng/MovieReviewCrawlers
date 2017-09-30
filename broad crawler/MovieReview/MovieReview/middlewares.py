# -*- encoding: utf-8 -*-

from fake_useragent import UserAgent
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware

class RotateUserAgentMiddleware(UserAgentMiddleware):
    def process_request(self, request, spider):
        user_agent = UserAgent()
        ua = user_agent.random
        if ua:
            request.headers.setdefault('User-Agent', ua)
