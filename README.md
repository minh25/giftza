#Giftza

# Introduction

Giftza is a project for crawling the data from [giftza.co](https://www.giftza.co/). 

Giftza is written base on Scrapy.

# Requirements

* Python 3

# If you want to customize the project, you need to know:

* Scrapy
* MongoDB

and so on...

# Install

Clone the project to your device, then:

    $ pip install -r requirements.txt

# Feature

* Get data of products in [giftza.co](https://www.giftza.co/)
    * Data of products: code, url, description, name, price, url of main image
* Customize proxy, prevent blocked status
* Connect to MongoDB

# Overview

* giftza
    * giftza
        * spiders
            * \__init__.py
            * product.py
                - __tags__
                - __department__
                - __product__
                - __color__
                - __sort__
        * \__init__.py
        * items.py
        * middlewares.py
            - ***CustomProxyMiddleware***
        * pipelines.py
            - ***MongoPipeline***
            - ***JsonWriterPipeline***
            - ***CsvWriterPipeline***
        * settings.py
            - __USER_AGENT__
            - __CONCURRENT_REQUESTS__
            - __MONGO_URI__
            - __MONGO_DATABASE__
            - __PROXY_FILE_NAME__
            - __USER_AGENT__
            - __DEFAULT_REQUEST_HEADERS__
            
    * main.py
        - run main.py to be easier in debug
    * README.md
    * requirements.txt
    * scrapy.cfg


# Usage

    $ scrapy crawl giftza
    
