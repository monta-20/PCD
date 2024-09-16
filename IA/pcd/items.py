# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import scrapy


class PcdItem(scrapy.Item):
    # define the fields for your item here like:
    date = scrapy.Field()
    close = scrapy.Field()
    open = scrapy.Field()
    high = scrapy.Field()
    low = scrapy.Field()
    companyName = scrapy.Field()
    news = scrapy.Field()

