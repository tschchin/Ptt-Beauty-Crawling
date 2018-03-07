import scrapy
import re

class PttSpider(scrapy.Spider):
	name = 'ptt_beauty'
	allowed_domains = ['ptt.cc']

	start_urls = [
		'https://www.ptt.cc/bbs/Beauty/index.html'
	]
	def parse(self, response):
		divs = response.xpath('//*[@id="main-container"]/div[2]')
		for div in divs:
			title = div.xpath('div[@class="r-ent"]/div[@class="title"]/a/text()').extract()
			date = div.xpath('div[@class="r-ent"]/div[@class="meta"]/div[@class="date"]/text()').extract()
			url = div.xpath('div[@class="r-ent"]/div[@class="title"]/a/@href').extract()
		with open('all_articles.txt', 'a') as f:
			for i in range(len(title)):
				if title[i].find("[公告]")== -1:
					f.write('{0},{1},{2}\n'.format(date[i],title[i],url[i]))
		if len(response.xpath('//*[@id="action-bar-container"]/div/div[2]/a[2]').extract()) > 0:
			path = response.xpath('//*[@id="action-bar-container"]/div/div[2]/a[2]/@href').extract()
			target_url = 'https://www.ptt.cc'
			url = target_url + path[0];
			yield scrapy.Request(url, callback=self.parse)
