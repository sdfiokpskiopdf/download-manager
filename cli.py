import click
from downloader import Downloader

@click.command()
@click.argument('url', type=click.Path())
@click.option('--threads', '-t', default=4, help='Number of threads used to split the download.', show_default=True)
@click.option('--name', '-n', type=click.Path(), help='Optional name of downloaded file.')
def main(url, threads, name):
	d = Downloader(url, threads, name, cli=True)
	d.download()

if __name__ == '__main__':
	main()
