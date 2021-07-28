import tkinter as tk
from downloader import Downloader
import multiprocessing
import threading
import time
import os

class AddFrame(tk.Frame):
	def __init__(self, parent, *args, **kwargs):
		tk.Frame.__init__(self, parent, *args, **kwargs)
		self.parent = parent

		self.options = [str(i) + " Threads" for i in range(1, multiprocessing.cpu_count()+1)]
		self.variable = tk.StringVar(self)
		self.variable.set(self.options[1])
		self.text = tk.Label(self, text="Download from URL:")
		self.urlEntry = tk.Entry(self)
		self.threadDrop = tk.OptionMenu(self, self.variable, *self.options)
		self.downloadButton = tk.Button(self, text="Download", command=lambda: threading.Thread(target=self.download).start())

		self.text.pack()
		self.urlEntry.pack(pady=5, fill="x", expand=True)
		self.threadDrop.pack(fill="x", expand=True)
		self.downloadButton.pack(pady=5, fill="x", expand=True)

	def download(self):
		url = self.urlEntry.get()
		threads = int(self.variable.get().split()[0])
		self.urlEntry.delete(0, 'end')
		self.variable.set(self.options[1])
		d = Downloader(url, threads)
		threading.Thread(target=d.download).start()
		self.parent.itemFrame.items.append(d)
		self.parent.itemFrame.draw_items()

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
				tk.Label(self, text=f"{item.file_name}").grid(row=i, column=0)
				tk.Label(self, text=f" {item.status}").grid(row=i, column=1)

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
	root.geometry('400x600')
	MainApplication(root).pack(side='top', fill='both', expand=True)
	root.mainloop()