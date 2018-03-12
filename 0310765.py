if __name__ == "__main__":
	import sys
	import subprocess
	func = sys.argv[1]

	#start_date =
	#end_date =

	if func=="crawl":
		subprocess.run(['scrapy','crawl','crawl_all_and_pop'])
	elif func=="push":
		subprocess.run(['scrapy','crawl','push_all','-a','start_date='+sys.argv[2],'-a','end_date='+sys.argv[3]])
		#subprocess.run(['scrapy','crawl','push_pop','-a','start_date='+sys.argv[2],'-a','end_date='+sys.argv[3]])
	elif func=='popular':
		subprocess.run(['scrapy','crawl','popular','-a','start_date='+sys.argv[2],'-a','end_date='+sys.argv[3]])
