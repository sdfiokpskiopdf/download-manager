import filecmp
import sys
import os 

testdir = os.path.dirname(__file__)
srcdir = '..'
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))

import downloader
import unittest

class TestDownloader(unittest.TestCase):

	TEST_URL = "https://file-examples-com.github.io/uploads/2017/10/file_example_JPG_1MB.jpg"
	TEST_THREADS = 4
	TEST_NAME = "TEST.jpg"
	TEST_FILE = os.path.join("assets", "TEST_IMAGE.jpg")

	def test_init(self):
		d = downloader.Downloader(self.TEST_URL, self.TEST_THREADS)

		self.assertEqual(d.request.status_code, 200)
		self.assertEqual(d.file_name, "file_example_JPG_1MB.jpg")

	def test_download(self):
		d = downloader.Downloader(self.TEST_URL, self.TEST_THREADS, self.TEST_NAME)
		d.download()

		self.assertTrue(filecmp.cmp(self.TEST_FILE, d.file_path))
		self.assertEqual(d.file_path.split("\\")[-1], self.TEST_NAME)
		self.assertEqual(d.t_length, self.TEST_THREADS)

	def test_convert_size(self):
		d = downloader.Downloader(self.TEST_URL, self.TEST_THREADS, self.TEST_NAME)
		
		self.assertEqual(d.convert_size(10_000), "9.77 KB")
		self.assertEqual(d.convert_size(10_000_000), "9.54 MB")
		self.assertEqual(d.convert_size(10_000_000_000), "9.31 GB")
		self.assertEqual(d.convert_size(10_000_000_000_000), "9.09 TB")
		self.assertEqual(d.convert_size(10_000_000_000_000_000), "8.88 PB")
		self.assertEqual(d.convert_size(10_000_000_000_000_000_000), "8.67 EB")
		self.assertEqual(d.convert_size(10_000_000_000_000_000_000_000), "8.47 ZB")
		self.assertEqual(d.convert_size(10_000_000_000_000_000_000_000_000), "8.27 YB")
		
		with self.assertRaises(ValueError):
			d.convert_size(1_210_000_000_000_000_000_000_000_001)
			d.convert_size(-1)

	def test_repr(self):
		d = downloader.Downloader(self.TEST_URL, self.TEST_THREADS, self.TEST_NAME)

		self.assertEqual(d.__repr__(), f"{self.TEST_NAME} {d.status}")

if __name__ == "__main__":
	unittest.main()



