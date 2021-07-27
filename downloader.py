import sys
import requests
import threading
from datetime import datetime

class Downloader:
	def __init__(self, url, threads, name=None, cli=False):

		self.url = url
		self.threads = threads
		
		# HEAD request of the URL, returning only header information such as status code, etc.
		try:
			request = requests.head(url)
		except:
			if cli:
				print('Request failed.')
				sys.exit()

		# If name is passed, use it as the file name, otherwise extract the file name from the URL.
		if name:
			self.file_name = name
		else:
			self.file_name = url.split('/')[-1]

		# Attempt to set the file size to the content length header. If this is not possible, we can not download from this URL.
		try:
			file_size = int(request.headers['content-length'])
		except:
			if cli:
				print('Error: invalid URL')
				sys.exit()

		# Specify the size of the chunks used for multithreaded downloading.
		self.part = int(file_size) / threads

		# Create a blank file the size of the content that will be downloaded.
		fp = open(self.file_name, 'w')
		fp.write('%uFFFD' * file_size)
		fp.close()

	def download(self):

		# Create threads for each part of the download.
		start_time = datetime.now()

		for i in range(self.threads):
			start = self.part * i
			end = start + self.part

			t = threading.Thread(target=self.handler, kwargs={'start': start, 'end': end, 'url': self.url, 'name': self.file_name})
			t.setDaemon(True) 
			t.start()

		# Wait for all of the threads to finish downloading.
		main_thread = threading.current_thread() 
		for t in threading.enumerate(): 

			if t is main_thread:
				continue

			t.join() 

		end_time = datetime.now()

		print(f'{self.file_name} downloaded in {(end_time - start_time).total_seconds()}')


	def handler(self, start, end, url, name):

		# Header specifying the chunk that this thread should download.
		headers = {'Range': 'bytes=%d-%d' % (start, end)}

		# Get request to initiate the download.
		request = requests.get(url, headers=headers, stream=True)

		# Open the file and write the request content to it.
		with open(name, "r+b") as f: 
			f.seek(int(start))
			var = f.tell() 
			f.write(request.content)