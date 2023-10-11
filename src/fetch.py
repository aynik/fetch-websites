import sys
import os
import logging
import argparse
from urllib.parse import urlparse
from lib.parser import extract_metadata, get_asset_urls
from lib.downloader import download_page, download_assets
from lib.utils import get_output_path, ensure_url_protocol


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Fetch and download web pages along with assets.')
    parser.add_argument('urls', metavar='URL', nargs='+', help='list of URLs to fetch')
    parser.add_argument('--metadata', action='store_true', help='display metadata of the fetched pages')

    return parser.parse_args()


def main():
    args = parse_args()

    for url in args.urls:
        url = ensure_url_protocol(url)
        output_path = get_output_path(url)
        logging.debug(f"Fetching {url}...")

        page_path = download_page(url, output_path)
        if page_path:
            logging.debug(f"Saved to {page_path}")

            with open(page_path, 'r', encoding='utf-8') as file:
                content = file.read()
                asset_url_map = {
                    k: v for k, v in get_asset_urls(content, url).items() if urlparse(v).netloc == urlparse(url).netloc
                }
                saved_assets = download_assets(asset_url_map, output_path)

                for original_url, local_path in saved_assets.items():
                    content = content.replace(original_url, local_path)

                with open(page_path, 'w', encoding='utf-8') as file:
                    file.write(content)

            if args.metadata:
                metadata = extract_metadata(content)
                print(f"site: {url}")
                print(f"num_links: {metadata['num_links']}")
                print(f"images: {metadata['num_images']}")
                print(f"last_fetch: {metadata['last_fetch']}")
        else:
            logging.error(f"Failed to download {url}.\n")


if __name__ == '__main__':
    main()
