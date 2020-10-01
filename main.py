from scrapy import cmdline


def main():
    cmdline.execute([
        'scrapy', 'crawl', 'giftza',
    ])

if __name__ == '__main__':
    main()
