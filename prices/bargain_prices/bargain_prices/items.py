# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item


class BargainPricesItem(Item):
    # define the fields for your item here like:
    next_page = scrapy.Field()
