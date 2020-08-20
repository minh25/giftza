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
color = [
    'black',
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
    'maroon'
]
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


def amount_of_item(response):
    """
    :param response:
    :return:
    return amount of product
    return -1, if can't find amount in menu pages or get error
    """
    try:
        str_item = response.xpath('//*[@id="main-content"]/div/div/div[2]/div/div[2]/div[1]/div/div[1]/div[2]/span/text()').get()
        if str_item == '1 item':
            return int(1)
        if str_item == '':
            return int(-1)
        str_item = str_item.replace(',', '')
        cnt_item = int(str_item[:-6])
        return cnt_item
    except Exception as error:
        return int(-1)


class UrlSpider(scrapy.Spider):
    name = 'product'
    allowed_domains = ['www.giftza.co']

    def start_requests(self):
        """
        yield menu pages with _department and _product
        """
        _tag = tags[5]
        for _department in department:
            for _product in product:
                url = url3(_tag, _department, _product)
                yield scrapy.Request(url=url, callback=self.parse_url_menu, dont_filter=True)

    def parse_url_menu(self, response):
        """
        with _department-and-_product-menu pages,
        yield menu pages
        if amount of product > 900, add _sort and _page (1->25) filter
        if amount of product <= 900, add _page (depending amount of product) filter
        """
        amount = amount_of_item(response)
        if amount == -1:
            yield scrapy.Request(url=response.url, callback=self.parse_url_menu, dont_filter=True)

        if amount > 0:
            page = int((amount + 35) / 36)
            for _page in range(1, min(26, page + 1), 1):
                if amount > 900:
                    for _sort in sort:
                        url = response.url + "/page/{}/sort/{}".format(_page, _sort)
                        yield scrapy.Request(url=url, callback=self.parse_url_product, dont_filter=True)
                        # yield {
                        #     "url": url,
                        # }
                else:
                    url = response.url + "/page/{}".format(_page)
                    yield scrapy.Request(url=url, callback=self.parse_url_product, dont_filter=True)
                    # yield {
                    #     "url": url,
                    # }

    def parse_url_product(self, response):
        """
        yield product
        """
        try:
            urls = response.xpath('//*[@id="main-content"]/div/div/div[2]/div[1]/div[2]/div[3]/div/div[1]/div/div/div/a[1]/@href').getall()
            for url in urls:
                code = url[-39:]
                if code not in set_code:
                    set_code.add(code)
                    yield scrapy.Request(url='https://www.giftza.co' + url, callback=self.parse_product, dont_filter=True)
                    # yield {
                    #     "url": url,
                    # }
            if len(urls) == 0:
                yield scrapy.Request(url=response.url, callback=self.parse_url_product, dont_filter=True)
        except Exception as error:
            yield scrapy.Request(url=response.url, callback=self.parse_url_product, dont_filter=True)


    def parse_product(self, response):
        """
        yield details of product
        """
        try:
            product_price = response.xpath('//span[@class="fs-xl color-red fw-bold lg:fs-2xl"]/span/text()').get()
            image_urls = response.xpath('//div[@class="p-a pin-t pin-l w-full h-full"]/img/@src').getall()
            product_name = response.xpath('//h1[@class="fs-md lg:fs-lg"]/span/text()').get()
            campaigns_details = response.xpath('//div[@class="px-1 pb-1 lg:px-0 bgc-white"]/div/div/text()').getall()

            if len(image_urls) == 0:
                yield scrapy.Request(url=response.url, callback=self.parse_product, dont_filter=True)
                return
        except Exception as error:
            yield scrapy.Request(url=response.url, callback=self.parse_product, dont_filter=True)
            return

        yield {
            'product price': product_price,
            'product_code': response.url[-39:],
            'image urls': image_urls,
            'product name': product_name,
            'campaigns details': campaigns_details,
        }
