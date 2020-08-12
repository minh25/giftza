import scrapy

# filter
tags = [
    'family-gift',
    'Relationship',
    'special-gifts',
    'mother-s-day',
    'father-s-day',
    'Holidays%20&%20Events'
]
department = [
    'men',
    'women',
    'youth',
    'assessories',
    'housewares'
]
product = [
    'shirt',
    'hoodie',
    'hat',
    'case',
    'sweatshirt',
    'longsleeve',
    'tanktop',
    'mug',
    'poster',
    'pillowcase',
    'blanket',
    'pillow'
]
color = ['black',
         'grey',
         'blue',
         'white',
         'red',
         'green',
         'blue-dark',
         'pink',
         'brown',
         'purple',
         'green-dark',
         'orange',
         'gold',
         'yellow',
         'maroon']
sort = [
    '-popularity',
    '-createdAt',
    'price',
    '-price'
]

# để tránh lặp lại product code
set_code = set()


# cho gọn
def url3(_tag, _department, _product):
    return "https://www.giftza.co/tags/{}/department/{}/product/{}".format(_tag, _department, _product)


# from string to int
def to_int(amount):
    try:
        amount = amount.replace(',', '')
        amount = int(amount)
    except:
        amount = int(0)
    return amount


class UrlSpider(scrapy.Spider):
    name = 'product'
    allowed_domains = ['www.giftza.co']

    def start_requests(self):
        _tag = tags[5]
        for _department in department:
            for _product in product:
                url = url3(_tag, _department, _product)
                yield scrapy.Request(url=url, callback=self.parse_url_menu, dont_filter=True)

    def parse_url_menu(self, response):
        if not response.xpath('//a[@class="fs-xs color-blue"]/@href').get():
            return scrapy.Request(url=response.url, callback=self.parse_url_menu, dont_filter=True)

        amount = response.xpath('//span[@class="color-primary fw-bold"]/text()').get()
        amount = to_int(amount)

        if amount > 0:
            page = int((amount + 35) / 36)
            for _page in range(1, min(26, page + 1), 1):
                if amount > 900:
                    for _sort in sort:
                        url = response.url + "/page/{}/sort/{}".format(_page, _sort)
                        yield scrapy.Request(url=url, callback=self.parse_url_product, dont_filter=True)
                else:
                    url = response.url + "/page/{}".format(_page)
                    yield scrapy.Request(url=url, callback=self.parse_url_product, dont_filter=True)

    def parse_url_product(self, response):
        if not response.xpath('//a[@class="fs-xs color-blue"]/@href').get():
            return scrapy.Request(url=response.url, callback=self.parse_url_product, dont_filter=True)

        urls = response.xpath(
            '//div[@class="w-1/2 lg:w-1/3 p-p5 lg:p-1"]/div/a[@class="d-ib br overflow-hidden bc-grey-300 '
            'cursor-pointer bw-1 bc-white:hover shadow-2:hover d-n lg:d-ib w-full bc-white"]/@href').getall()

        for url in urls:
            code = url[-39:]
            if code not in set_code:
                set_code.add(code)
                yield scrapy.Request(url='https://www.giftza.co' + url, callback=self.parse_product, dont_filter=True)

    def parse_product(self, response):
        if not response.xpath('//a[@class="fs-xs color-blue"]/@href').get():
            return scrapy.Request(url=response.url, callback=self.parse_product, dont_filter=True)

        product_price = response.xpath('//span[@class="fs-xl color-red fw-bold lg:fs-2xl"]/span/text()').get()
        image_urls = response.xpath('//div[@class="p-a pin-t pin-l w-full h-full"]/img/@src').getall()
        product_name = response.xpath('//h1[@class="fs-md lg:fs-lg"]/span/text()').get()
        campaigns_details = response.xpath('//div[@class="px-1 pb-1 lg:px-0 bgc-white"]/div/div/text()').getall()

        yield {
            'product price': product_price,
            'product_code': response.url[-39:],
            'image urls': image_urls,
            'product name': product_name,
            'campaigns details': campaigns_details,
        }
