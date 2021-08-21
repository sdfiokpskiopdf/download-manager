import click
from downloader import Downloader


@click.command()
@click.argument("url", type=click.Path())
@click.option(
    "--threads",
    "-t",
    default=4,
    help="Number of threads used to split the download.",
    show_default=True,
)
@click.option(
    "--name", "-n", type=click.Path(), help="Optional name of downloaded file."
)
@click.option(
    "--path",
    "-p",
    type=click.Path(exists=True),
    help="Optional directory to store file. Default: downloads folder",
)
def main(url, threads, name, path):
    d = Downloader(url, threads, name, path, cli=True)
    d.download()


if __name__ == "__main__":
    main()
