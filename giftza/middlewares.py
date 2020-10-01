# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import logging
import random


# useful for handling different item types with a single interface


class GiftzaSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class GiftzaDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class CustomProxyMiddleware(object):
    """
    choose a random proxy each request
    a raised-exception proxy will have a low rate to be chosen

    Setting:
    PROXY_FILE_NAME: giftza.settings.PROXY_FILE_NAME
    """

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            proxy_file_name=crawler.settings.get('PROXY_FILE_NAME')
        )

    def __init__(self, proxy_file_name):
        self.ip_addresses = []

        proxies = open(proxy_file_name, "r").readlines()
        for proxy in proxies:
            self.ip_addresses.append(proxy)

        self.ip_pass = []
        self.ip_fall = []

        for _ in range(1, len(self.ip_addresses) + 1, 1):
            self.ip_pass.append(int(1))
            self.ip_fall.append(int(1))

    def rand_ip(self):
        while True:
            ip_index = random.randrange(0, len(self.ip_addresses))
            var = self.ip_pass[ip_index] / self.ip_fall[ip_index]

            if var >= 0.25:
                return ip_index

            self.ip_pass[ip_index] += 1

    def process_request(self, request, spider):
        proxy_index = self.rand_ip()
        request.meta['proxy'] = self.ip_addresses[proxy_index]
        request.meta['proxy_index'] = proxy_index
        request.meta['download_timeout'] = 30
        logging.log(logging.WARNING, request.meta['proxy'])
        return None

    def process_response(self, request, response, spider):
        if response.status != 200:
            return request.copy()
        self.ip_pass[request.meta['proxy_index']] += 3
        return response

    def process_exception(self, request, exception, spider):
        self.ip_fall[request.meta['proxy_index']] += 20
        return request.copy()
