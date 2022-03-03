import scrapy
import scrapy_splash
from scrapy_splash import SplashRequest


class TimesofmaltaSpider(scrapy.Spider):
    name = 'timesofmalta'
    allowed_domains = ['https://timesofmalta.com']
    start_urls = ['https://timesofmalta.com/']

    # def __init__(self) -> None:
    #     super().__init__()

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url=url, callback=self.parse, args={'wait': 2})

    def parse(self, response):
        main_news = response.css("div.sw-InnerGrid a::attr(href)").getall()
        
        for news in main_news:
            pass

