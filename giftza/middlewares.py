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

    def __init__(self):
        self.ip_addresses = [
            "http://37.97.206.153:5836",
            "http://37.97.135.70:5836",
            "http://92.245.142.215:8080",
            "http://41.254.46.103:8080",
            "http://89.208.35.81:3128",
            "http://84.110.62.250:8080",
            "http://185.114.157.233:5836",
            "http://212.83.152.130:5836",
            "http://173.249.33.59:59635",
            "http://194.44.225.34:53281",
            "http://138.117.85.113:999",
            "http://168.228.51.238:8080",
            "http://5.252.179.10:3128",
            "http://95.68.115.202:53281",
            "http://213.108.5.224:3128",
            "http://37.97.206.158:5836",
            "http://91.224.182.49:8080",
            "http://77.247.127.45:8118",
            "http://217.174.149.233:5836",
            "http://138.117.85.17:999",
            "http://173.249.33.59:51216",
            "http://91.206.30.218:3128",
            "http://45.139.203.41:3128",
            "http://179.189.226.186:8080",
            "http://45.175.255.3:999",
            "http://46.18.210.233:5836",
            "http://185.126.165.131:5836",
            "http://37.97.135.190:5836",
            "http://31.44.12.116:5836",
            "http://31.134.135.124:22113",
            "http://193.169.20.102:5836",
            "http://185.184.243.199:5836",
            "http://37.97.206.156:5836",
            "http://45.181.224.18:999",
            "http://5.187.52.68:5836",
            "http://190.214.20.58:999",
            "http://46.18.210.234:5836",
            "http://79.104.25.218:8080",
            "http://196.216.220.204:36739",
            "http://190.61.45.254:999",
            "http://90.183.101.238:45277",
            "http://151.106.52.27:5836",
            "http://186.96.117.26:999",
            "http://45.174.254.10:999",
            "http://41.33.179.195:8080",
            "http://191.97.14.21:11201",
            "http://173.249.33.59:64135",
            "http://212.129.37.169:5836",
            "http://186.7.66.236:999",
            "http://65.182.5.212:8080",
            "http://187.188.168.56:9991",
            "http://189.203.79.106:30391",
            "http://81.198.66.166:8080",
            "http://173.249.33.59:54462",
            "http://185.232.66.126:5836",
            "http://92.64.58.74:8080",
            "http://185.25.206.192:3128",
            "http://91.142.12.34:8081",
            "http://185.184.243.198:5836",
            "http://5.187.52.69:5836",
            "http://213.120.213.242:8081",
            "http://45.139.203.85:3128",
            "http://193.8.46.7:8080",
            "http://217.174.149.245:5836",
            "http://138.0.89.162:8080",
            "http://193.176.212.195:8080",
            "http://194.87.232.33:5836",
            "http://158.51.201.249:8080",
            "http://186.7.205.30:999",
            "http://91.226.243.34:8080",
            "http://189.201.242.225:999",
            "http://190.2.210.98:8080",
            "http://37.120.168.223:8888",
            "http://80.243.158.6:8080",
            "http://95.0.66.109:8080",
            "http://41.86.251.62:8080",
            "http://193.169.20.101:5836",
            "http://188.68.240.147:5836",
            "http://187.60.46.229:8080",
            "http://37.97.190.117:5836",
            "http://5.252.179.16:3128",
            "http://95.141.36.112:8686",
            "http://190.214.45.206:999",
            "http://200.73.129.185:8080",
            "http://186.167.48.234:3128",
            "http://37.97.135.99:5836",
            "http://31.44.12.119:5836",
            "http://24.245.100.212:48678",
            "http://193.169.20.98:5836",
            "http://186.235.159.138:8403",
            "http://173.249.33.59:49277",
            "http://45.7.135.53:999",
            "http://190.83.32.4:8080",
            "http://213.58.202.70:54214",
            "http://151.106.52.28:5836",
            "http://191.102.125.245:8080",
            "http://86.123.166.109:8080",
            "http://191.102.94.94:8080",
            "http://193.169.20.99:5836",
            "http://187.62.213.110:46269",
            "http://89.223.20.202:5836",
            "http://41.65.243.66:8080",
            "http://5.249.152.108:5836",
            "http://201.149.100.32:8085",
            "http://92.244.143.86:7890",
            "http://93.191.102.81:3128",
            "http://186.190.224.202:999",
            "http://92.119.222.1:8080",
            "http://185.21.66.212:8080",
            "http://5.187.52.70:5836",
            "http://151.106.18.183:5836",
            "http://82.177.38.195:8080",
            "http://163.172.198.112:5836",
            "http://212.129.30.85:5836",
            "http://185.114.157.232:5836",
            "http://5.252.179.11:3128",
            "http://52.179.18.244:8080",
            "http://212.83.166.94:5836",
            "http://178.208.131.68:8080",
            "http://188.212.102.252:5836",
            "http://212.115.235.12:81",
            "http://45.174.77.113:999",
            "http://93.118.32.243:5836",
            "http://212.129.38.111:5836",
            "http://176.56.236.158:3128",
            "http://185.186.81.155:999",
            "http://190.110.222.51:999",
            "http://185.184.243.196:5836",
            "http://207.244.250.124:10393",
            "http://89.221.54.114:8080",
            "http://185.117.9.210:8080",
            "http://85.214.244.174:3128",
            "http://78.8.188.200:32040",
            "http://91.194.247.247:3333",
            "http://194.8.146.167:38479",
            "http://45.177.16.135:999",
            "http://189.174.169.114:8080",
            "http://91.206.148.243:53292",
            "http://89.108.112.1:8014",
            "http://185.97.135.20:8080",
            "http://45.237.184.193:999",
            "http://213.238.167.120:5836",
            "http://62.118.131.240:3128",
            "http://190.61.42.218:9991",
            "http://212.83.144.125:5836",
            "http://31.44.12.117:5836",
            "http://94.246.158.238:8080",
            "http://147.75.51.179:3128",
            "http://167.250.65.246:8080",
            "http://200.73.129.185:80",
            "http://185.25.206.192:8080",
            "http://181.48.88.238:8080",
            "http://31.44.12.118:5836",
            "http://173.249.33.59:50387",
            "http://91.133.0.229:8080",
            "http://69.62.21.80:8080",
            "http://188.212.102.227:5836",
            "http://200.69.94.202:999",
            "http://195.140.226.244:8080",
            "http://178.252.80.226:34730",
            "http://85.221.247.234:8080",
            "http://189.203.73.102:9991",
            "http://46.221.9.22:8080",
            "http://193.169.20.100:5836",
            "http://138.0.228.25:999",
            "http://81.144.138.35:3128",
            "http://46.151.108.6:47481",
            "http://45.236.120.241:999",
            "http://178.132.220.241:8080",
            "http://185.69.28.213:8080",
            "http://95.163.87.74:41890",
            "http://87.255.27.169:3128",
            "http://46.149.80.207:33835",
            "http://5.252.179.17:3128",
            "http://151.106.52.29:5836",
            "http://46.219.85.64:8080",
            "http://189.198.250.253:80",
            "http://81.17.131.59:8080",
            "http://185.200.36.120:8080",
            "http://157.100.9.219:999"
        ]
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
