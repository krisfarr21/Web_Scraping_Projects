from multiprocessing.connection import wait
import scrapy
import scrapy_splash
from scrapy_splash import SplashRequest        
from collections import defaultdict
        
class TimesofmaltaSpider(scrapy.Spider):
    name = 'timesofmalta'
    allowed_domains = ['timesofmalta.com']
    start_urls = ['https://timesofmalta.com/']

    def parse(self, response):
        return SplashRequest(url=self.start_urls[0], callback=self.parse_cats, args={'wait': 4})
    
    def parse_cats(self, response):
        self.logger.info("Visited %s", response.url)
        # getting categories names and amending dictionary storing every link for that category
        self.categories_names = response.css('div.na-PrimaryNavigation_Main a::text').getall()[1:]
        self.category_article_links = {k.lower():[] for k in self.categories_names}
        self.logger.info(self.category_article_links)
        self.categories_links = response.css('div.na-PrimaryNavigation_Main a::attr(href)').getall()[2:] # removed empty link + latest(for now)
        self.logger.info("Categories %s", self.categories_links) 
        for cat in self.categories_links[1:3]:
            yield SplashRequest(url=cat, callback=self.parse_links, args={'wait': 5})
    
    def parse_links(self, response):
        # current page and category
        self.current_category = response.css('div.li-ListingArticles_head.wi-WidgetHeader > h1::text').get()
        self.current_page = response.css('div.pi-Pagination > span.current::text').get()
        # article links
        links = list(set([link for link in response.css('div.li-Listing_Main a::attr(href)').getall() if 'articles/author' not in link])) # getting all links, removing authors' webpages
        links = [link for link in links if 'cta_comments' not in link] # removing hrefs to access comments
        articles_links = [link for link in links if '/page:' not in link] # removing pagination links from article links
        # self.logger.info("Articles: %s", articles_links)
        self.category_article_links[self.current_category].extend(articles_links) # adding links to dictionary
        # pages = sorted([self.start_urls[0]+link[1:] for link in links if '/page:' in link]) # saving pagination links and adding base_url to paginated links
        # yield {
        #     'category article links': self.category_article_links,
        #     'current category': self.current_category }
        #     'current page': current_page,
        #     'links': articles_links}
        next_page = response.css('span.next > a::attr(href)').get()
        if next_page:
            self.logger.info("REQUESTING NEXT PAGE")
            yield SplashRequest(url=self.start_urls[0]+next_page[1:], callback=self.parse_links, args={'wait':5})
        else:
            self.logger.info("REQUESTING LINKS IN CATEGORY")
            yield {'category_articles' : self.category_article_links}
            for url in self.category_article_links[self.current_category]:
                yield SplashRequest(url=url, callback=self.parse_info, args={'wait': 5})

    def parse_info(self, response):
        yield {
            'url' : response.url,
            'current category': self.current_category,
            'current page': self.current_page,
            'title' : response.css('h1.wi-WidgetSubCompType_13-title::text').get(),
            'subtitle' :  response.css('h2.wi-WidgetSubCompType_13-subtitle::text').get()

        }
            # yield {
        #     'links': (current_category, articles_links, len(articles_links))}
        # yield {'page' : (current_category, pages)}
