from unicodedata import category
import scrapy
from multiprocessing.sharedctypes import Value
from scrapy_splash import SplashRequest
import time
# import os
import regex as re
import subprocess, argparse
from bargain_prices.spiders.links.hrefs import *
import playwright
from scrapy_playwright.page import PageCoroutine

class GreensPricesSpider(scrapy.Spider):
    name = 'greens'
    start_urls = greens_categories()
    next_page = None

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url=url, callback=self.parse, args={'wait': 2})

    def parse(self, response):
        print(self.logger.info('A response from %s just arrived!', response.url))
        # dropdown = response.css("select.search-drop-down")[0]
        # category = dropdown.xpath('//*[@id="ddHeaderSearchDropdown"]/option[18]/text()').extract()
        products = response.css('div.col-md-2.col-sm-3.shop-grid-item')
        for product in products:
            yield { 
            # 'category' : re.search("(?<==).*(?=&)", response.url).group(0),
            'product_name' : product.css('a.title.product-title::text').get(),
            'product_price' : product.css('div.current::text').get(),
            'product_type' : product.css('a.tag::text').get(),
            'offer_type': product.css('div.hot-mark.purple::text').get(),
            'offer': product.css('div.special-offer-text::text').get()
            }
        self.next_page = response.xpath('//*[@id="pnlPagesTop"]/a[4]/@href').extract()
        if self.next_page:
            try:
                yield SplashRequest(url=self.next_page[0], callback=self.parse, args={'wait': 2})
            except: 
                print("Next page not found")

class ArkadiaPricesSpider(scrapy.Spider):
    name = 'arkadia'

    start_urls = ['https://malta.arkadiafoodstore.com/product-category/bakery/']

    def start_requests(self):
        yield scrapy.Request(
            url=self.start_urls[0],
            meta=dict(
                playwright=True,
                playwright_include_page=True,
                playwright_page_coroutines=[
                    PageCoroutine("wait_for_selector", "body > div.container > div > div.container > div > div.col-sm-12.col-md-9 > div > nav"),
                    PageCoroutine("evaluate", "window.scrollBy(0, document.body.scrollHeight)"),
                    PageCoroutine("wait_for_selector", "body > div.container > div > div.container > div > div.col-sm-12.col-md-9 > div > nav.woocommerce-custom-loadmore.no-more"),  # 10 per page
                ],
            ),
        )
    async def parse(self, response):
        yield {
            'title' : response.css('title::text').get(),
            'product_name' : response.css('h2.woocommerce-loop-product__title::text').getall()
        }


# def main():
#     subprocess.run(["scrapy", "crawl", "prices", "-a", "category=bakery"], capture_output=True)
#     parser = argparse.ArgumentParser()
#     parser.add_argument("--supermarket", type=str, 
#                         choices=['greens'], help="choose supermarket to get its data")
#     parser.add_argument("-v", "--verbose", help="increase output verbosity",
#                     action="store_true")
#     args = parser.parse_args()
#     # if args.verbose:
#     #     print("verbosity turned on")
#     subprocess.run(f"scrapy crawl prices {args.supermarket}_prices -a category=bakery", shell=True)

# if __name__ == '__main__':
#     main()