import scrapy
from scrapy_splash import SplashRequest

class prices_spider(scrapy.Spider):
    name =  'prices'

    def start_requests(self):

        urls = []
        for page in range(1, 18):
            urls.append(f'https://www.greens.com.mt/products?cat=fruitsandvegetables&pg={page}&sort=Position&sortd=Asc')
        for url in urls:
            yield SplashRequest(url=url, callback=self.parse, args={'wait': 8})
    
    def parse(self, response, **kwargs):
        
        products = response.css('div.col-md-2.col-sm-3.shop-grid-item')
        for item in products:
            yield {
            'product_name' : item.css('a.title.product-title::text').get(),
            'product_price' : item.css('div.current::text').get(),
            }
