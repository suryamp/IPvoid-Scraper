import scrapy

from ipvoidscraper.items import scan_results
import urllib2,re

class ipvoidSpider(scrapy.Spider):
	name = "ipvoidchecker"
	allowed_domains = ["ipvoid.com"]
	start_urls=[]

	def __init__(self):
		for line in open('./ip.txt', 'r').readlines():
			# get rid of newline characters
			stripped_line = line.strip()
			self.start_urls.append('http://www.ipvoid.com/scan/%s' % stripped_line)

	def parse(self, response):
		item = scan_results()

		item['ip'] = response.selector.css('#left > table:nth-child(6) > tbody > tr:nth-child(3) > td:nth-child(2) > strong::text').extract_first()
		item['last_updated_time'] = response.selector.css('#left > table:nth-child(6) > tbody > tr:nth-child(1) > td:nth-child(2)::text').extract_first()
		item['safe_status'] = response.selector.css('#left > table:nth-child(6) > tbody > tr:nth-child(2) > td:nth-child(2) > span::text').extract_first()
		item['link_to_scan_results'] = response.url
		
		pattern = re.compile("seconds")

		# if report is upto date, pass to output	
		if pattern.match(str(item['last_updated_time'])) is not None:
			yield item
		# if report is not, refresh by "clicking" the update report button
		else:
			urllib2.urlopen('http://www.ipvoid.com/update-report/'+ str(item['ip'])).read()
			yield scrapy.Request(response.url,callback=self.parse)