from multiprocessing.sharedctypes import Value
import scrapy
from scrapy_splash import SplashRequest
import os
import regex as re
import subprocess
from links.get_hrefs import green_categories

# from bargain_prices.items import BargainPricesItem # for future itemloader

# NEXT TASK: send requests for each category + pages

class greens(scrapy.Spider):
    name = 'greens_prices'
    
    urls_categories = green_categories()
    
    def __init__(self, category=None, *args, **kwargs):
        super(greens, self).__init__(*args, **kwargs)
        category = self.urls_categories[category]
        self.start_urls = category

    def start_requests(self):
        yield SplashRequest(url=self.start_urls, callback=self.parse, args={'wait': 4})

    def parse(self, response):
        print(self.logger.info('A response from %s just arrived!', response.url))
        for product in response.css('div.col-md-2.col-sm-3.shop-grid-item'):
            yield { 
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

def main():
    subprocess.run(["scrapy", "crawl", "prices", "-a", "category=bakery"], capture_output=True)

if __name__ == '__main__':
    main()
