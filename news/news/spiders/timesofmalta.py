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
        return SplashRequest(url=self.start_urls[0], callback=self.parse_categories, args={'wait': 4})

    
    def parse_categories(self, response):
        self.logger.info("Visited %s", response.url)
        # getting categories names and amending dictionary storing every link for that category
        self.categories_names = response.css('div.na-PrimaryNavigation_Main a::text').getall()[1:]
        self.logger.info("CATEGORY NAMES %s", self.categories_names)

        # links for categories
        self.categories_links = response.css('div.na-PrimaryNavigation_Main a::attr(href)').getall()[2:] # removed empty link + latest(for now)
        self.logger.info("CATEGORY LINKS %s", self.categories_links)

        # dictionary containing links for each page of each category (including the first page)

        # self.category_page_links = {k.lower():[v] for (k,v) in (self.categories_names, self.categories_links)}
        zipped = list(zip(self.categories_names, [[link] for link in self.categories_links]))
        self.category_page_links = {k:v for (k, v) in zipped}
        self.logger.info("CATEGORY PAGE LINKS %s", self.category_page_links)

        # dictionary containing links for each article of each category
        self.category_article_links = {k.lower():[] for k in self.categories_names}
        self.logger.info("CATEGORY ARTICLE LINKS %s", self.category_article_links)
        
        for cat in self.categories_links[1:2]:
            yield SplashRequest(url=cat, callback=self.parse_page_links, args={'wait': 5})

    def parse_page_links(self, response):
        # current page and category
        self.current_category = response.css('div.li-ListingArticles_head.wi-WidgetHeader > h1::text').get()
        self.current_page = response.css('div.pi-Pagination > span.current::text').get()

        
        # article links
        links = list(set([link for link in response.css('div.li-Listing_Main a::attr(href)').getall() if 'articles/author' not in link])) # getting all links, removing authors' webpages
        links = [link for link in links if 'cta_comments' not in link] # removing hrefs to access comments
        articles_links = [link for link in links if '/page:' not in link] # removing pagination links from article links
        self.logger.info("Articles: %s", articles_links)

        # appending articles from each page to self.category_article_links
        for link in articles_links:
            if link[:5] == 'https':
                self.category_article_links[self.current_category].append(link)

        # checking if next page exists
        next_page = response.css('span.next > a::attr(href)').get()
        if next_page is not None: # and int(next_page[next_page.index(':')+1:]) < 100: # scrape only the next 100 pages 
            yield SplashRequest(self.start_urls[0]+next_page[1:], callback=self.parse_page_links, args={'wait': 5, "timeout": 3000})
        else:
            for article_link in self.category_article_links[self.current_category]:
                yield SplashRequest(url=article_link, callback=self.parse_info, args={'wait': 5, "timeout": 3000})
                # self.logger.info("AFTER SCRAPING EVERYTHING %s", self.category_article_links, len(self.category_article_links[self.current_category]))
    

    def parse_info(self, response):
        yield {
            'url' : response.url,
            'current category': self.current_category,
            'current page': self.current_page,
            'title' : response.css('h1.wi-WidgetSubCompType_13-title::text').get(),
            'subtitle' :  response.css('h2.wi-WidgetSubCompType_13-subtitle::text').get(),
            'tags' : response.css('div.ar-ArticleHeader-Standard_sub.ar-ArticleHeader-Standard_sub-1.wi-WidgetSubCompType_13 \
             > div.wi-WidgetKeywords-container > button.light::text').getall(), # had to specify page due to equivalent html tags at the end of the page
            'time to read' : response.css('span.wi-WidgetMeta-readingTime > span::text').get(),
            'article' : response.css('div.ar-Article_Content > p::text').getall()
        
        }


   # def parse_info(self, response):


    #     self.category_article_links[self.current_category].extend(articles_links) # adding links to dictionary
    #     # pages = sorted([self.start_urls[0]+link[1:] for link in links if '/page:' in link]) # saving pagination links and adding base_url to paginated links
    #     # yield {
    #     #     'category article links': self.category_article_links,
    #     #     'current category': self.current_category }
    #     #     'current page': current_page,
    #     #     'links': articles_links}
    #     next_page = response.css('span.next > a::attr(href)').get()
    #     if next_page:
    #         self.logger.info("REQUESTING NEXT PAGE")
    #         yield SplashRequest(url=self.start_urls[0]+next_page[1:], callback=self.parse_links, args={'wait':5})
    #     else:
    #         self.logger.info("REQUESTING LINKS IN CATEGORY")
    #         yield {'category_articles' : self.category_article_links}
    #         print("LENGTH OF ELECTION 2022 ARTICLES", self.category_article_links[self.current_category])
    #         for url in self.category_article_links[self.current_category]:
    #             yield SplashRequest(url=url, callback=self.parse_info, args={'wait': 5})