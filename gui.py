import tkinter as tk
import tkinter.filedialog
from downloader import Downloader
import multiprocessing
import subprocess
import threading
import time
import os

class AddFrame(tk.Frame):
	def __init__(self, parent, *args, **kwargs):
		tk.Frame.__init__(self, parent, *args, **kwargs)
		self.parent = parent
		self.download_path = None

		self.options = [str(i) + " Threads" for i in range(1, multiprocessing.cpu_count()+1)]
		self.variable = tk.StringVar(self)
		self.variable.set(self.options[1])
		self.text = tk.Label(self, text="Download from URL:")
		self.urlEntry = tk.Entry(self)
		self.nameText = tk.Label(self, text="Name of file:")
		self.nameEntry = tk.Entry(self)
		self.threadDrop = tk.OptionMenu(self, self.variable, *self.options)
		self.setButton = tk.Button(self, text="📁 Download Location", command=lambda: threading.Thread(target=self.set_location).start())
		self.downloadButton = tk.Button(self, text="Download", height=2, command=lambda: threading.Thread(target=self.download).start())

		self.text.grid(row=0, column=0)
		self.urlEntry.grid(row=0, column=1, columnspan=2, sticky="ew")
		self.nameText.grid(row=1, column=0)
		self.nameEntry.grid(row=1, column=1, columnspan=2, sticky="ew", pady=5)
		self.threadDrop.grid(row=2, column=0, sticky="ew")
		self.setButton.grid(row=2, column=1, columnspan=2, sticky="ew")
		self.downloadButton.grid(row=3, column=0, columnspan=3, sticky="ew", pady=5)

		for i in range(3):
			self.grid_rowconfigure(i, weight=1)
			self.grid_columnconfigure(i, weight=1)

	def download(self):
		url = self.urlEntry.get()
		name = self.nameEntry.get()
		threads = int(self.variable.get().split()[0])
		self.variable.set(self.options[1])
		d = Downloader(url, threads, name, self.download_path, gui=True)
		self.urlEntry.delete(0, 'end')
		self.nameEntry.delete(0, 'end')
		threading.Thread(target=d.download).start()
		self.parent.itemFrame.items.append(d)
		self.parent.itemFrame.draw_items()

	def set_location(self):
		self.download_path = tk.filedialog.askdirectory()

class ItemFrame(tk.Frame):
	def __init__(self, parent, *args, **kwargs):
		tk.Frame.__init__(self, parent, *args, **kwargs)
		self.parent = parent

		self.items = []
		self.prev_items = []
		self.status = ""
		self.prev_status = ""
		t = threading.Thread(target=self.update)
		t.start()

	def draw_items(self):

		try:
			self.status = list(reversed(self.items))[0].status
		except:
			self.status = ""

		if self.prev_items != self.items or self.status != self.prev_status:

			self.prev_status = self.status
			self.prev_items = self.items.copy()

			for widget in self.winfo_children():
				widget.grid_forget()

			print("updating...")
			for i, item in enumerate(reversed(self.items)):
				if len(item.file_name) > 25:
					fileName = item.file_name[:25] + "..."
				else:
					fileName = item.file_name
				tk.Label(self, text=f"{fileName}").grid(row=i, column=0, padx=5)
				tk.Label(self, text=f"{item.status}").grid(row=i, column=1)
				tk.Button(self, text="📁", command=lambda i=item.file_path: subprocess.Popen(r'explorer /select,"{path}"'.format(path=i))).grid(row=i, column=2, padx=5)
				tk.Label(self, text=f"{item.file_size}").grid(row=i, column=3)

	def update(self):
		while True:
			self.draw_items()
			time.sleep(0.5)

class MainApplication(tk.Frame):
	def __init__(self, parent, *args, **kwargs):
		tk.Frame.__init__(self, parent, *args, **kwargs)
		self.parent = parent 
		self.addFrame = AddFrame(self)
		self.itemFrame = ItemFrame(self)

		self.addFrame.pack(side="top", fill="x", expand=False, padx=20, pady=5)
		self.itemFrame.pack(side="bottom", fill="y", expand=True)

def on_closing():
	os._exit(1)


if __name__ == '__main__':
	root = tk.Tk()
	root.protocol("WM_DELETE_WINDOW", on_closing)
	root.title("Download Manager")
	root.geometry('500x300')
	MainApplication(root).pack(side='top', fill='both', expand=True)
	root.mainloop()