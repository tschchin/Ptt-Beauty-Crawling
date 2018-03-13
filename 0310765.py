if __name__ == "__main__":
	import sys
	import subprocess
	func = sys.argv[1]

	if func=="crawl":
		subprocess.run(['scrapy','crawl','crawl_all_and_pop'])
	elif func=="push":
		subprocess.run(['scrapy','crawl','push_all','-a','start_date='+sys.argv[2],'-a','end_date='+sys.argv[3]])
	elif func=='popular':
		subprocess.run(['scrapy','crawl','popular','-a','start_date='+sys.argv[2],'-a','end_date='+sys.argv[3]])
	elif func=='keyword':
		subprocess.run(['scrapy','crawl','keyword','-a','keyword='+sys.argv[2],'-a','start_date='+sys.argv[3],'-a','end_date='+sys.argv[4]])
