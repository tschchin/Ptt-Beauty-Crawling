import scrapy
import re
import sys
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
import operator

class Ptt_Keyword_Spider(scrapy.Spider):
	name = 'keyword'
	allowed_domains = ['ptt.cc']
	start_urls = []
	pic_format = ['jpg','jpeg','png','gif']

	def parse(self,response):
		content = response.xpath('//*[@id="main-container"]')
		text = content.xpath('descendant::*/text()').extract()
		ele_text = []
		for i in text:
			i = i.replace('\n','')
			if i.find('※ 發信站: 批踢踢實業坊(ptt.cc)')!=-1 :
				break
			else:
				if i.find(self.keyword)!=-1:
					contents = content.xpath('descendant::*/a')
					#print(contents)
					for c in contents:
						if len(c.xpath('text()').extract())>0: # ignore []
							url = c.xpath('text()').extract()[0]
							if any( p_f in url[-6:].lower() for p_f in self.pic_format):
								self.popular.append(url)
					break
		if self.i < len(self.url)-1:
			self.i += 1
			print(self.i)
			yield scrapy.Request(self.url[self.i],self.parse)

	def __init__(self, keyword=None,start_date=None, end_date=None, *args, **kwargs):
		dispatcher.connect(self.spider_closed, signals.spider_closed)
		super(Ptt_Keyword_Spider, self).__init__(*args, **kwargs)
		self.keyword = keyword
		self.url = [] # the page to crawl
		self.popular = [] # the resault
		self.start_date = start_date
		self.end_date = end_date
		self.i = 0
		with open('all_articles.txt','r') as f:
			for line in f:
				date,*_,url = line.split(',')
				if int(start_date)<=int(date) and int(end_date)>=int(date):
					self.url.append(url[:-1])
			self.start_urls.append(self.url[0])

	def spider_closed(self, spider):
		with open('keyword('+self.keyword+')'+'['+self.start_date+'-'+self.end_date+'].txt','w') as f:
			pass
		with open('keyword('+self.keyword+')'+'['+self.start_date+'-'+self.end_date+'].txt','a') as f:
			for i in self.popular:
				f.write(i+'\n')
