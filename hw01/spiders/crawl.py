# Download all and popular articles for 2017 ptt_Beauty.
# author: Tsai,Cheng Chin (for Data Science hw01)

import scrapy
import re
import sys

class ARTICLEItem(scrapy.Item):
	date = scrapy.Field()
	title = scrapy.Field()
	url = scrapy.Field()
	popular = scrapy.Field()
	year = scrapy.Field()

class PttSpider(scrapy.Spider):
	name = 'crawl_all_and_pop'
	allowed_domains = ['ptt.cc']

	start_urls = [
		'https://www.ptt.cc/bbs/Beauty/index2000.html'
	]
	# clear the file
	# with open('all_articles.txt', 'w'):
	# 	pass
	# with open('all_popular.txt', 'w'):
	#	pass

	pg = 2000

	def parse(self, response):
		articles = response.xpath('//*[@id="main-container"]/div[2]/div[@class="r-ent"]')

		# list for crawled data
		dates = []
		titles = []
		urls = []
		populars = []

		# get [date],[title],[url] and [popular]
		for article in articles:
			dates.extend([''.join(article.xpath('div[@class="meta"]/div[@class="date"]/text()').extract())])
			titles.extend([''.join(article.xpath('div[@class="title"]/a/text()').extract())])
			urls.extend([''.join(article.xpath('div[@class="title"]/a/@href').extract())])
			populars.extend([''.join(article.xpath('div[@class="nrec"]/span/text()').extract())])

		# change date format
		dates = self.date_format(dates)

		# crawl all articles
		#with open('all_articles.txt', 'a') as f_all:
		if self.pg==2000:
			p = 13
			st = len(titles)
		elif self.pg==2352:
			p = 0
			st = 14
		else:
			p = 0
			st = len(titles)
		self.pg += 1
		while p < st:
			url = 'https://www.ptt.cc'+urls[p]
			if  titles[p].find('Yoonjoo') == -1 and titles[p].find('[公告]') == -1 and len(urls[p])!=0:
				with open('all_articles.txt', 'a') as f_all:
					f_all.write('{0},{1},{2}\n'.format(dates[p],titles[p],url))
				if populars[p] == "爆":
					with open('all_popular.txt', 'a') as f_pop:
						f_pop.write('{0},{1},{2}\n'.format(dates[p],titles[p],url))
				print(dates[p],titles[p])
			p += 1

		# iterate to next page
		if len(response.xpath('//*[@id="action-bar-container"]/div/div[2]/a[3]').extract()) > 0:
			path = response.xpath('//*[@id="action-bar-container"]/div/div[2]/a[3]/@href').extract()
			target_url = 'https://www.ptt.cc'
			ng = target_url + path[0]
			if int(ng[-9:-5])<=2352:
				yield scrapy.Request(ng, callback=self.parse)

	def date_format(self, dates):
		new_dates = []
		for date in dates:
			date = date.replace('/','')
			date = date.replace(' ','')
			new_dates.append(date)
		return new_dates
	'''
	def get_year(self,response):
		year = response.meta['year']
		time = response.xpath('//*[@id="main-content"]/div[4]/span[2]/text()').extract()
		time = time[0]
		year['year'] = time[-4:]
		if time[-4:]!='2016' and time[-4:]!='2018':
			with open('all_articles.txt', 'a') as f_all:
				f_all.write('{0},{1},{2}\n'.format(response.meta['date'],response.meta['title'],response.meta['url']))
			if (response.meta['popular']=="爆"):
				with open('all_popular.txt', 'a') as f_pop:
					f_pop.write('{0},{1},{2}\n'.format(response.meta['date'],response.meta['title'],response.meta['url']))
		#print(time[-4:],response.meta['date'],response.meta['title'])
		yield year
	'''
