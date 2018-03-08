import scrapy
import re

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

	def date_format(self, dates):
		new_dates = []
		for date in dates:
			date = date.replace('/','')
			date = date.replace(' ','')
			new_dates.append(date)
		return new_dates


	def parse(self, response):
		articles = response.xpath('//*[@id="main-container"]/div[2]/div[@class="r-ent"]')

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
		'''
		print(self.date_format(dates))
		print(titles[0])
		print(urls)
		print(populars)
		'''
		print(len(urls))
		print(titles[13].find('[公告]'))

		# change date format
		dates = self.date_format(dates)

		# crawl all articles
		with open('all_articles.txt', 'a') as f_all:
			for i in range(len(titles)):
				# ignore [公告]
				if  titles[i].find('[公告]') == -1 and len(urls[i])!=0:
					f_all.write('{0},{1},{2}\n'.format(dates[i],titles[i],'https://www.ptt.cc'+urls[i]))

		# crawl popular articles
		with open('all_popular.txt', 'a') as f_pop:
			for i in range(len(titles)):
				# choose popular
				if (populars[i]=="爆") and (titles[i].find('[公告]') == -1) and len(urls[i])!=0:
					f_pop.write('{0},{1},{2}\n'.format(dates[i],titles[i],'https://www.ptt.cc'+urls[i]))

		# iterate to next page
		if len(response.xpath('//*[@id="action-bar-container"]/div/div[2]/a[2]').extract()) > 0:
			path = response.xpath('//*[@id="action-bar-container"]/div/div[2]/a[2]/@href').extract()
			target_url = 'https://www.ptt.cc'
			url = target_url + path[0];
			yield scrapy.Request(url, callback=self.parse)
