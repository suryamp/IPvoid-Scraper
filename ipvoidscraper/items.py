# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class scan_results(scrapy.Item):
    last_updated_time = scrapy.Field()
    safe_status = scrapy.Field()
    link_to_scan_results = scrapy.Field()
    ip = scrapy.Field()
