import os
import sys
import math
import requests
import threading
from datetime import datetime
from tkinter import messagebox

class Downloader:
	def __init__(self, url, threads, name=None, cli=False):

		self.url = url
		self.threads = threads
		self.storedThreads = []
		self.status = "waiting..."
		
		# HEAD request of the URL, returning only header information such as status code, etc.
		try:
			request = requests.head(url)
		except:
			if cli:
				print('Error: Can not establish a connection.')
			else:
				messagebox.showerror("Error", "Can not establish a connection")

			sys.exit()


		# If name is passed, use it as the file name, otherwise extract the file name from the URL.
		if name:
			if "." not in name and not cli:
				messagebox.showerror("Error", "Please include a file extension in your file name.")
				sys.exit()
			else:
				self.file_name = name
		else:
			self.file_name = url.split('/')[-1]

		# Attempt to set the file size to the content length header. If this is not possible, we can not download from this URL.
		try:
			file_size = int(request.headers['content-length'])
			self.file_size = self.convert_size(file_size)
		except Exception as e:
			if cli:
				print('Error: Can not download from this URL')
			else:
				print(e)
				messagebox.showerror("Error", "Can not download from this URL")

			sys.exit()
				

		# Specify the size of the chunks used for multithreaded downloading.
		self.part = int(file_size) / threads

		# Create a blank file the size of the content that will be downloaded.
		self.file_path = self.get_download_path() + "\\" + self.file_name
		fp = open(self.file_path, 'w')
		fp.write('%uFFFD' * file_size)
		fp.close()

	def download(self):

		self.status = "downloading..."

		# Create threads for each part of the download.
		start_time = datetime.now()

		for i in range(self.threads):
			start = self.part * i
			end = start + self.part

			t = threading.Thread(target=self.handler, kwargs={'start': start, 'end': end, 'url': self.url, 'name': self.file_name})
			t.setDaemon(True) 
			t.start()

			self.storedThreads.append(t)

		# Wait for all of the threads to finish downloading.
		main_thread = threading.current_thread() 
		for t in self.storedThreads:
			t.join()

		end_time = datetime.now()
		self.status = "downloaded"
		print(f'{self.file_name} downloaded in {(end_time - start_time).total_seconds()}')


	def handler(self, start, end, url, name):

		# Header specifying the chunk that this thread should download.
		headers = {'Range': 'bytes=%d-%d' % (start, end)}

		# Get request to initiate the download.
		request = requests.get(url, headers=headers, stream=True)

		# Open the file and write the request content to it.
		with open(self.file_path, "r+b") as f: 
			f.seek(int(start))
			var = f.tell() 
			f.write(request.content)

	def get_download_path(self):

		# Returns the default downloads path for linux or windows
		if os.name == 'nt':
			import winreg
			sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
			downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'
			with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
				location = winreg.QueryValueEx(key, downloads_guid)[0]
			return location
		else:
			return os.path.join(os.path.expanduser('~'), 'downloads')

	def convert_size(self, size_bytes):
		if size_bytes == 0:
			return "0B"
		size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
		i = int(math.floor(math.log(size_bytes, 1024)))
		p = math.pow(1024, i)
		s = round(size_bytes / p, 2)
		return "%s %s" % (s, size_name[i])

	def __repr__(self):
		return f"{self.file_name} {self.status}"