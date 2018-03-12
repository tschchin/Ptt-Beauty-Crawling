# author: Tsai,Cheng Chin (for Data Science hw01)

import scrapy
import re
import sys
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
import operator


class Ptt_Push_ALL_Spider(scrapy.Spider):
	name = 'push_all'
	allowed_domains = ['ptt.cc']
	start_urls = []

	def parse(self,response):
		pushs = response.xpath('//*[@id="main-content"]/div[@class="push"]')
		for push in pushs:
			push_tag = push.xpath("span[contains(concat(' ',normalize-space(@class),'hl push-tag'),'')]/text()").extract()
			if push_tag[0].replace(" ","")=="推":
				self.like += 1
				if push_tag[1] not in self.author_like:
					self.author_like[push_tag[1]] = 1
				else:
					self.author_like[push_tag[1]] += 1
			elif push_tag[0].replace(" ","")=="噓":
				if push_tag[1] not in self.author_boo:
					self.author_boo[push_tag[1]] = 1
				else:
					self.author_boo[push_tag[1]] += 1
				self.boo += 1

	def __init__(self, start_date=None, end_date=None, *args, **kwargs):
		dispatcher.connect(self.spider_closed, signals.spider_closed)
		super(Ptt_Push_ALL_Spider, self).__init__(*args, **kwargs)
		self.like = 0
		self.boo = 0
		self.author_like = {}
		self.author_boo = {}
		self.start_date = start_date
		self.end_date = end_date
		with open('all_articles.txt','r') as f:
			line = f.readline()
			while len(line)>0:
				date = int(line.split(',',2)[0])
				url = line.split(',',2)[2][:-1]
				if int(start_date)<=date and int(end_date)>=date:
					self.start_urls.append(url)
				line = f.readline()

	def spider_closed(self, spider):
		with open('push['+self.start_date+'-'+self.end_date+'].txt','w') as f:
			pass
		with open('push['+self.start_date+'-'+self.end_date+'].txt','a') as f:
			f.write('all like: {0}\n'.format(str(self.like)))
			f.write('all boo: {0}\n'.format(str(self.boo)))
			# print('all like: '+str(self.like))
			# print('all boo: '+str(self.boo))
			sorted_like = sorted(self.author_like, key=lambda key: (-self.author_like[key],key))
			sorted_boo = sorted(self.author_boo, key=lambda key: (-self.author_boo[key],key))
			if len(sorted_like)<10:
				ll = len(sorted_like)
			else:
				ll= 10
			if len(sorted_boo)<10:
				lb = len(sorted_boo)
			else:
				lb= 10
			for i in range(ll):
				# print("like #"+str(i+1)+": "+sorted_like[i] + " " + str(self.author_like[sorted_like[i]]))
				f.write("like #{0}: {1}  {2}\n".format(str(i+1),sorted_like[i],str(self.author_like[sorted_like[i]])))
			for i in range(lb):
				f.write("boo #{0}: {1}  {2}\n".format(str(i+1),sorted_boo[i],str(self.author_boo[sorted_boo[i]])))
				# print("boo #"+str(i+1)+": "+sorted_boo[i] + " " + str(self.author_boo[sorted_boo[i]]))
