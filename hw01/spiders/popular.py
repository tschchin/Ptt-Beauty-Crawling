import scrapy
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher

class Ptt_Popular_Spider(scrapy.Spider):
	name = 'popular'
	allowed_domains = ['ptt.cc']
	start_urls = []
	pic_format = ['jpg','jpeg','png','gif']
	def parse(self,response):
		content = response.xpath('//*[@id="main-container"]')
		contents = content.xpath('descendant::*/a')
		for c in contents:
			if len(c.xpath('text()').extract())>0:
				url = c.xpath('text()').extract()[0]
				#print(url)
				if any( p_f in url[-6:].lower() for p_f in self.pic_format):
					self.pic_url.append(url)
		if self.pg_count < (len(self.url)-1):
			self.pg_count += 1
			yield scrapy.Request(self.url[self.pg_count])

	def __init__(self, start_date=None, end_date=None, *args, **kwargs):
		dispatcher.connect(self.spider_closed, signals.spider_closed)
		super(Ptt_Popular_Spider, self).__init__(*args, **kwargs)
		self.popular = 0
		self.pic_url = []
		self.url = []
		self.pg_count = 0
		self.start_date = start_date
		self.end_date = end_date
		with open('all_popular.txt','r') as f:
			for line in f:
				date,*_,url = line.split(',')
				if int(start_date)<=int(date) and int(end_date)>=int(date):
					self.url.append(url[:-1]) # ignore '\n'
					self.popular += 1
		self.start_urls.append(self.url[0])

	def spider_closed(self, spider):
		with open('popular['+self.start_date+'-'+self.end_date+'].txt','w') as f:
			pass
		with open('popular['+self.start_date+'-'+self.end_date+'].txt','a') as f:
			f.write('number of popular articles: {0}\n'.format(self.popular))
			for url in self.pic_url:
				f.write(url+'\n')
