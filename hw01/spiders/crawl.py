# Download all and popular articles for 2017 ptt_Beauty.
# author: Tsai,Cheng Chin (for Data Science hw01)

import scrapy
import re

class ARTICLEItem(scrapy.Item):
	date = scrapy.Field()
	title = scrapy.Field()
	url = scrapy.Field()
	popular = scrapy.Field()
	year = scrapy.Field()

class PttSpider(scrapy.Spider):
	name = 'ptt_beauty'
	allowed_domains = ['ptt.cc']

	start_urls = [
		'https://www.ptt.cc/bbs/Beauty/index.html'
	]
	# clear the file
	with open('all_articles.txt', 'w'):
		pass
	with open('all_popular.txt', 'w'):
		pass



	def parse(self, response):
		articles = response.xpath('//*[@id="main-container"]/div[2]/div[@class="r-ent"]')

		# if year == 2017
		stop = 0

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

		for i in range(len(titles)):
			url = 'https://www.ptt.cc'+urls[i]
			if  titles[i].find('[公告]') == -1 and len(urls[i])!=0:
				#f_all.write('{0},{1},{2}\n'.format(dates[i],titles[i],'https://www.ptt.cc'+urls[i]))
				request = scrapy.Request(url,callback=self.get_year,meta={'date':dates[i],'title':titles[i],'url':url,'popular':populars[i]})
				request.meta['year']=ARTICLEItem(date=dates[i],title=titles[i],url=url,popular=populars[i])
				yield request

		# iterate to next page
		if len(response.xpath('//*[@id="action-bar-container"]/div/div[2]/a[2]').extract()) > 0:
			path = response.xpath('//*[@id="action-bar-container"]/div/div[2]/a[2]/@href').extract()
			target_url = 'https://www.ptt.cc'
			ng = target_url + path[0];
			yield scrapy.Request(ng, callback=self.parse)

	def date_format(self, dates):
		new_dates = []
		for date in dates:
			date = date.replace('/','')
			date = date.replace(' ','')
			new_dates.append(date)
		return new_dates

	def get_year(self,response):
		year = response.meta['year']
		time = response.xpath('//*[@id="main-content"]/div[4]/span[2]/text()').extract()
		time = time[0]
		year['year'] = time[-4:]
		if time[-4:]=='2017' and int(time[-4:])>=2017:
			with open('all_articles.txt', 'a') as f_all:
				f_all.write('{0},{1},{2}\n'.format(response.meta['date'],response.meta['title'],response.meta['url']))
			if (response.meta['popular']=="爆"):
				with open('all_popular.txt', 'a') as f_pop:
					f_pop.write('{0},{1},{2}\n'.format(response.meta['date'],response.meta['title'],response.meta['url']))
		if int(time[-4:])<2017:
			print('!',time[-4:],response.meta['date'],response.meta['title'])
			#raise scrapy.exceptions.CloseSpider("success 2017")
		else:
			print(time[-4:],response.meta['date'],response.meta['title'])
		yield year
