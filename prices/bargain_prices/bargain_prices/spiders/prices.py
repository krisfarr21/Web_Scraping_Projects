import scrapy
from scrapy_splash import SplashRequest
from bargain_prices.items import BargainPricesItem

class prices_spider(scrapy.Spider):
    name =  'prices'
    # def start_requests(self):
    urls = []
    def __init__(self, name='prices', **kwargs):
        super().__init__(name, **kwargs)
        self.start_urls = ['''http://localhost:8050/render.html?url=
                    https://www.greens.com.mt/products?cat=fruitsandvegetables&wait=4''']

        # iterating through page numbers instead of following pagination
        #         # for page in range(1, 20):
        #     urls.append(f'https://www.greens.com.mt/products?cat=fruitsandvegetables&pg={page}&sort=Position&sortd=Asc')
        # for url in urls:
        # yield SplashRequest(url=start_url, callback=self.parse, args={'wait': 4})
    
    def parse(self, response, **kwargs):

        for product in response.css('div.col-md-2.col-sm-3.shop-grid-item'):
            yield { 
            'product_name' : product.css('a.title.product-title::text').get(),
            'product_price' : product.css('div.current::text').get(),
            }
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
