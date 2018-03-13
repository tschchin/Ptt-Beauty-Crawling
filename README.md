# Data Science (hw01): Ptt Crawling

Use scrapy to crawl https://www.ptt.cc/bbs/Beauty/index.html  for 2017 articles and analysis.

## Getting Started
###1. Crawl
```
python3 0310765.py crawl
```
 * Input: N/A
 * Content
	* crawl all articles in 2017
	* ignore [公告]
 * Output:
 	* all_articles.txt (all articles)
	* all_popular.txt (all popular articles)
 * file format:
 	* [date],[title],[URL]
###2. Push
```
python3 0310765.py push start_date end_date
```
 * Input:
 	* start_date
	* end_date
	e.g.,python3 0310765.py push 101 830
 * Content
 	* find all articles between start_date and end_date:
		* number of like and boo
		* the user id who like most all_articles
		* the user id who boo most all_articles
 * Output:
 	* push[start_date-end_date].txt
 * File Format:
	* all like: n
	  all boo: n
	  like #rank: [user_id] [number of like]  (rand 1-10)
	  boo #rank: [user_id] [number of boo] (rand 1-10)
###3. Popular
```
python3 0310765.py popular start_date end_date
```
 * Input:
 	* start_date
 	* end_date
 * Content:
 	* find all articles between start_date and end_date:
		* output the number of popular all_articles
		* output all URL of pictures in popular articles
		* all url of pictures end up with jpg,jpeg,png,gif
 * Output
 	* popular[start_date-end_date].txt
 * File Format:
 	* number of popular articles: n
	* each line with one url
###4. Keyword
```
python3 0310765.py keyword [keyword] start_date end_date
```
 * Input:
 	* [keyword] (keyword to find)
	* start_date
	* end_date
 * Content:
 	* find all url of pictures with articles include keyword during start_date and end_date
 * Output:
 	* keyword([keyword])[start_date-end_date].txt

## Prerequisites

 * python3
 * scrapy

## Authors

 * Tsai, Cheng Chin
