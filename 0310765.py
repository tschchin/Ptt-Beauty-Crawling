if __name__ == "__main__":
	import sys
	import subprocess
	func = sys.argv[1]
	if func=="crawl":
		subprocess.run(['scrapy','crawl','ptt_beauty'])
	#elif func=='push':
