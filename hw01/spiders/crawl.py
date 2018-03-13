# Download all and popular articles for 2017 ptt_Beauty.
# author: Tsai,Cheng Chin (for Data Science hw01)

import scrapy
import re
import sys
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher

class Ptt_Crawl_Spider(scrapy.Spider):
	name = 'crawl_all_and_pop'
	allowed_domains = ['ptt.cc']
	start_urls = [
		'https://www.ptt.cc/bbs/Beauty/index2000.html'
	]#'https://www.ptt.cc/bbs/Beauty/index2000.html']
	exclude_pgs = [
		'https://www.ptt.cc/bbs/Beauty/M.1490936972.A.60D.html',
		'https://www.ptt.cc/bbs/Beauty/M.1494776135.A.50A.html',
		'https://www.ptt.cc/bbs/Beauty/M.1503194519.A.F4C.html',
		'https://www.ptt.cc/bbs/Beauty/M.1504936945.A.313.html',
		'https://www.ptt.cc/bbs/Beauty/M.1505973115.A.732.html',
		'https://www.ptt.cc/bbs/Beauty/M.1507620395.A.27E.html',
		'https://www.ptt.cc/bbs/Beauty/M.1510829546.A.D83.html',
		'https://www.ptt.cc/bbs/Beauty/M.1512141143.A.D31.html'
	]

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
		for p in range(len(titles)):
			url = 'https://www.ptt.cc' + urls[p]
			if not url in self.exclude_pgs:
				if int(response.request.url[-9:-5]) == 2000 and int(dates[p])>200:
					pass
				elif int(response.request.url[-9:-5]) == 2352 and int(dates[p])<1200:
					pass
				elif titles[p][:4] != '[公告]' and len(urls[p])!=0:
					self.dates.append(dates[p])
					self.titles.append(titles[p])
					self.urls.append(url)
					self.populars.append(populars[p])
		if self.np <= 2351:
			self.np += 1
			yield scrapy.Request('https://www.ptt.cc/bbs/Beauty/index'+str(self.np)+'.html')

	def date_format(self, dates):
		new_dates = []
		for date in dates:
			date = date.replace('/','')
			date = date.replace(' ','')
			new_dates.append(date)
		return new_dates

	def __init__(self, *args, **kwargs):
		dispatcher.connect(self.spider_closed, signals.spider_closed)
		super(Ptt_Crawl_Spider, self).__init__(*args, **kwargs)
		with open('all_articles.txt', 'w'):
		 	pass
		with open('all_popular.txt', 'w'):
			pass
		self.dates = []
		self.titles = []
		self.urls = []
		self.populars = []
		self.np = 2000

	def spider_closed(self, spider):
		f_all =  open('all_articles.txt', 'a')
		f_pop = open('all_popular.txt', 'a')
		for p in range(len(self.titles)):
			f_all.write('{0},{1},{2}\n'.format(self.dates[p],self.titles[p],self.urls[p]))
			if self.populars[p] == "爆":
				f_pop.write('{0},{1},{2}\n'.format(self.dates[p],self.titles[p],self.urls[p]))
		f_all.close()
		f_pop.close()
