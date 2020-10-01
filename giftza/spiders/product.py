import scrapy
import json

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
    'accessories',
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

# set of product
set_of_product = set()
test_code_product = set()


def amount_of_item(response):
    """
    get the amount of product to calculate the amount of page
    :param response: response of a menu
    :return:
    return amount of product
    return -1, if can't find amount in menu pages or get error
    """
    try:
        str_item = response.xpath(
            '//*[@id="main-content"]/div/div/div[2]/div/div[2]/div[1]/div/div[1]/div[2]/span/text()').get()
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
    name = 'giftza'
    allowed_domains = ['www.giftza.co']
    allowed_http_status_codes = [200, 400]

    def start_requests(self):
        """
        yield menu pages with _tag, _department and _product
        """
        _tag = tags[5]
        for _department in department:
            for _product in product:
                url = "https://www.giftza.co/tags/{}/department/{}/product/{}".format(_tag, _department, _product)
                yield scrapy.Request(url=url,
                                     callback=self.parse_url_menu,
                                     dont_filter=True,
                                     meta={'tag': _tag,
                                           'department': _department,
                                           'product': _product})

    def parse_url_menu(self, response):
        """
        yield menu pages with _tag, _department, _product, _sort, _page
        if amount of product > 900, add 4-_sort and _page (1->25) filter
        if amount of product <= 900, add 1-_sort and _page filter
        """
        amount = amount_of_item(response)
        if amount == -1:
            yield scrapy.Request(url=response.url,
                                 callback=self.parse_url_menu,
                                 dont_filter=True,
                                 meta=response.request.meta)

        if amount > 0:
            page = int((amount + 35) / 36)
            for _page in range(1, min(26, page + 1), 1):
                if amount > 900:
                    for _sort in sort:
                        url = response.url + "/page/{}/sort/{}".format(_page, _sort)
                        yield scrapy.Request(url=url,
                                             callback=self.parse_url_product,
                                             dont_filter=True,
                                             meta={'tag': response.request.meta['tag'],
                                                   'department': response.request.meta['department'],
                                                   'product': response.request.meta['product'],
                                                   'sort': _sort,
                                                   'page': _page})
                else:
                    url = response.url + "/page/{}/sort/{}".format(_page, sort[0])
                    yield scrapy.Request(url=url,
                                         callback=self.parse_url_product,
                                         dont_filter=True,
                                         meta={'tag': response.request.meta['tag'],
                                               'department': response.request.meta['department'],
                                               'product': response.request.meta['product'],
                                               'sort': sort[0],
                                               'page': _page})

    def parse_url_product(self, response):
        """
        yield a POST request to get description of product
        :param response: response of a menu
        """
        try:
            # <script>      window.__INITIAL_STATE__ = {"localeData":{...},"meta":{}};    </script>
            # script_text = "      window.__INITIAL_STATE__ = {"localeData":{...},"meta":{}};    "
            script_text = response.xpath('//body/script/text()').get()

            # json_text = ""localeData":{...},"meta":{}"
            json_text = script_text[34:-6]

            json_data = json.loads(json_text)

            check_error = True

            ids = []

            dict_of_36_product = {}

            for iD, details in json_data["vias"]["CampaignProduct"]["docs"]["id"].items():
                dict_of_36_product[details['doc']['code']] = {
                    'id': iD,
                    'name': details['doc']['names']['design'],
                    'price': details['doc']['price'],
                    'image': details['doc']['images'][0]['prefix'] + '/regular.jpg',
                    'code': details['doc']['code'],
                    'campaignUrl': details['doc']['campaignUrl'],
                    'campaignId': details['doc']['campaignId'],
                    'url': 'https://www.giftza.co/campaigns/sort/{}/page/{}/department/{}/product/{}/tags/{}/{}'
                           '?retailProductCode={}'.format(response.request.meta['sort'],
                                                          response.request.meta['page'],
                                                          response.request.meta['department'],
                                                          response.request.meta['product'],
                                                          response.request.meta['tag'],
                                                          details['doc']['campaignUrl'],
                                                          details['doc']['code'])
                }
                ids.append(details['doc']['campaignId'])
                check_error = False

            if check_error:
                raise Exception('=))')
            else:
                yield scrapy.Request(url="https://www.giftza.co/rest/campaigns/bulk",
                                     method='POST',
                                     body=json.dumps(ids),
                                     callback=self.parse_product,
                                     headers={'Content-Type': 'application/json'},
                                     dont_filter=True,
                                     meta={'dict_of_36_product': dict_of_36_product})

        except Exception as error:
            yield scrapy.Request(url=response.url,
                                 callback=self.parse_url_product,
                                 dont_filter=True,
                                 meta=response.request.meta)

    def parse_product(self, response):
        """
        yield details of product
        :param response: response of the POST request
        """
        try:
            json_data = json.loads(response.text)
            dict_of_36_product = response.request.meta['dict_of_36_product']

            check_error = True

            for details in json_data:
                check_error = False
                campaignId = details['_id']
                for iD, product in dict_of_36_product.items():
                    if product['campaignId'] == campaignId:
                        product['description'] = details['description']

            if check_error:
                raise Exception('=))')

            for iD, product in dict_of_36_product.items():
                if product['code'] not in set_of_product:
                    set_of_product.add(product['code'])
                    yield {
                        'code': product['code'],
                        'url': product['url'],
                        'description': product['description'],
                        'name': product['name'],
                        'price': product['price'],
                        'image': product['image'],
                    }
        except Exception as error:
            yield scrapy.Request(url="https://www.giftza.co/rest/campaigns/bulk",
                                 method='POST',
                                 body=response.request.body,
                                 callback=self.parse_product,
                                 headers={'Content-Type': 'application/json'},
                                 dont_filter=True,
                                 meta=response.request.meta)
