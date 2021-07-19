# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class DangdangItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    book_img = scrapy.Field()
    book_title = scrapy.Field()
    book_author = scrapy.Field()
    book_desc= scrapy.Field()
    book_price = scrapy.Field()
    book_pulish_date = scrapy.Field()
    book_press  = scrapy.Field()
    b_cate = scrapy.Field()
    m_cate = scrapy.Field()
    s_cate = scrapy.Field()
    s_href = scrapy.Field()
    pass
