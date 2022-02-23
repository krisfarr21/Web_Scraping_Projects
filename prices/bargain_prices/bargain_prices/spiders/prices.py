from multiprocessing.sharedctypes import Value
import scrapy
from scrapy_splash import SplashRequest
import os
# from bargain_prices.items import BargainPricesItem # for future itemloader

# NEXT TASK: send requests for each category + pages

class prices_spider(scrapy.Spider):
    name = 'prices'
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    FILE = os.path.join(THIS_FOLDER, 'greens_links.txt')
    
    start_urls = []

    with open(FILE, 'r') as f:
        lines = f.readlines()
        URL_NUMBER = '&pg=1&sort=Position&sortd=Asc'
        urls = [link.strip('\n') for link in lines]
        for link in urls:
            start_urls.append(link+URL_NUMBER)
        start_urls = start_urls[2:4]
        # URL_NUMBER not identified in list comprehension????
        # start_urls = [link + URL_NUMBER for link in start_urls]

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url=url, callback=self.parse, args={'wait': 4})

    def parse(self, response):
        print("START-URLS ---> ", self.start_urls)
        current_category = response.xpath('//*[@id="ddHeaderSearchDropdown"]/option[10]/text()').extract()[0]
        for product in response.css('div.col-md-2.col-sm-3.shop-grid-item'):
            yield { 
            'category' : current_category,
            'product_name' : product.css('a.title.product-title::text').get(),
            'product_price' : product.css('div.current::text').get(),
            'product_type' : product.css('a.tag::text').get(),
            'offer_type': product.css('div.hot-mark.purple::text').get(),
            'offer': product.css('div.special-offer-text::text').get()
            }
        next_page = response.xpath('//*[@id="pnlPagesTop"]/a[4]/@href').extract()
        try:
            print("PAGNA LI JMISS--->",next_page, len(next_page), type(next_page[0]))
        except:
            print("PAGNA LI JMISS--->",next_page, len(next_page), type(next_page))
        # arbitrary number - last page of above xpath was outputting '#' instead of None
        if len(next_page[0]) > 5 and next_page[0] is not None: 
            yield SplashRequest(url=next_page[0], callback=self.parse, args={'wait': 4})