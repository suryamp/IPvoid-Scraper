import scrapy

from ipvoidscraper.items import scan_results
import urllib2,re,requests

class ipvoidSpider(scrapy.Spider):
	name = "ipvoidchecker"
	allowed_domains = ["ipvoid.com"]
	start_urls=[]

	# TODO define list of ip addresses here in case report does not exist
	def __init__(self):
		for line in open('./ip.txt', 'r').readlines():
			# get rid of newline characters
			stripped_line = line.strip()
			self.start_urls.append('http://www.ipvoid.com/scan/%s' % stripped_line)

	def parse(self, response):
		
		# create a scan_results instance to populate
		item = scan_results()

		item['ip'] = response.selector.css('#left > table:nth-child(6) > tbody > tr:nth-child(3) > td:nth-child(2) > strong::text').extract_first()
		item['last_updated_time'] = response.selector.css('#left > table:nth-child(6) > tbody > tr:nth-child(1) > td:nth-child(2)::text').extract_first()
		item['safe_status'] = response.selector.css('#left > table:nth-child(6) > tbody > tr:nth-child(2) > td:nth-child(2) > span::text').extract_first()
		item['link_to_scan_results'] = response.url
		
		# this regex query finds 'seconds' when we look in the "Analysis Date" field
		pattern = re.compile("seconds")

		# if report contains an ip, ip has been scanned before
		if item['ip']:

			# is Analysis Date was seconds ago, yield item
			if pattern.match(str(item['last_updated_time'])) is not None:
				yield item
			
			# if report is not, refresh by "clicking" the update report button
			else:
				urllib2.urlopen('http://www.ipvoid.com/update-report/'+ str(item['ip'])).read()
				yield scrapy.Request(response.url,callback=self.parse)
		
		# if ip field is void, we need to ping server for a brand new support
		else:
			# TODO make post call after fetching the ip address
			url = 'http://www.ipvoid.com'
			ip_address_pattern = re.compile("^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$");
			match = re.search(ip_address_pattern,response.url)
			values = {'ip' : match.re.pattern}
			data = urllib.urlencode(values)
			req = urllib2.Request(url, data)
			response = urllib2.urlopen(req)
			the_page = response.read()
			yield scrapy.Request(response.url,callback=self.parse)