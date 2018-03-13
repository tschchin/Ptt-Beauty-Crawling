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
					self.url.append(url)

	def __init__(self, start_date=None, end_date=None, *args, **kwargs):
		dispatcher.connect(self.spider_closed, signals.spider_closed)
		super(Ptt_Popular_Spider, self).__init__(*args, **kwargs)
		self.popular = 0
		self.url = []
		self.start_date = start_date
		self.end_date = end_date
		with open('all_popular.txt','r') as f:
			line = f.readline()
			while len(line)>0:
				date = int(line.split(',',2)[0])
				url = line.split(',',2)[2][:-1]
				if int(start_date)<=date and int(end_date)>=date:
					self.start_urls.append(url)
					self.popular += 1
				line = f.readline()

	def spider_closed(self, spider):
		with open('popular['+self.start_date+'-'+self.end_date+'].txt','w') as f:
			pass
		with open('popular['+self.start_date+'-'+self.end_date+'].txt','a') as f:
			f.write('number of popular articles: {0}\n'.format(self.popular))
			for url in self.url:
				f.write(url+'\n')
