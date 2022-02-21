import scrapy
from scrapy_splash import SplashRequest
from bargain_prices.items import BargainPricesItem # for future itemloader

class prices_spider(scrapy.Spider):
    name =  'prices'
    local_host = 'http://localhost:8050/render.html?url='
    # next task: change start url to greens homepage
    start_url = 'https://www.greens.com.mt/products?cat=fruitsandvegetables'

    def start_requests(self):
        yield SplashRequest(url=self.start_url, callback=self.parse, args={'wait': 4})

    # next task: get links for categories and check if you can use response.follow

    def check_next_url(self, response):
        '''
        Checks if next page exists
        '''
        next_page = response.xpath('//*[@id="pnlPagesTop"]/a[4]/@href').extract()
        if next_page:
            return next_page[0]
        return False
    
    def parse(self, response, **kwargs):
        # yield requests for each page
        for product in response.css('div.col-md-2.col-sm-3.shop-grid-item'):
            yield { 
            'product_name' : product.css('a.title.product-title::text').get(),
            'product_price' : product.css('div.current::text').get(),
            }
        next_page = self.check_next_url(response=response)
        if next_page:
            yield SplashRequest(url=next_page, callback=self.parse, args={'wait': 4})

        # next_page = response.css('#pnlPagesBottom > a:nth-child(5)::attr(href)').extract_first()
        # if next_page:
        #     yield response.follow(url= 'http://localhost:8050/render.html?url=' + next_page + '&wait=4', 
        #     callback=self.parse)
        # products = response.css('div.col-md-2.col-sm-3.shop-grid-item')
        # for product in products:
        #     item = { 
        #     'product_name' : product.css('a.title.product-title::text').get(),
        #     'product_price' : product.css('div.current::text').get(),
        #     }
        #     yield item

        # following pagitation link
        # next_page_url = response.css('#pnlPagesBottom > a:nth-child(5)::attr(href)').extract_first()
        # if next_page_url:
        #     # print(next_page_url)
        #     yield SplashRequest(url=next_page_url, callback=self.parse, args={'wait': 4}),

        

        # item = BargainPricesItem()
        # item['next_page'] =  response.xpath('//*[@id="pnlPagesBottom"]/a[4]/@href')
        # print("ITEM-->",item)
        # print("ITEM_NEXT_PAGE-->",item['next_page'].get(), type(item['next_page']))
        # if item['next_page'] is not None:
        #     yield response.follow(item['next_page'], self.parse)
