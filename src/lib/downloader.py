import os
import json
import requests
import logging
from urllib.parse import urlparse


def fetch_and_save(url, filename):
    """Fetch the URL and save the content to the specified filename."""
    headers = json.loads(os.environ.get("HTTP_HEADERS", "{}"))
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        binary = 'image' in response.headers.get('content-type', '').lower()
        mode = 'wb' if binary else 'w'
        content = response.content if binary else response.text

        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, mode) as file:
            file.write(content)

        return filename

    except requests.RequestException as e:
        logging.error(f"Error downloading {url}. Error: {e}")
        return None


def download_page(url, output_path):
    """Download a web page and save it to the output directory."""
    domain_name = urlparse(url).netloc
    filename = os.path.join(output_path, "index.html")
    return fetch_and_save(url, filename)


def download_assets(asset_url_map, output_path):
    """Download assets (like images, scripts, styles) and save them to the output directory."""
    saved_assets = {}
    for original_url, full_url in asset_url_map.items():
        asset_name = os.path.basename(urlparse(full_url).path)
        filename = os.path.join(output_path, asset_name)
        result = fetch_and_save(full_url, filename)
        
        if result:
            saved_assets[original_url] = asset_name

    return saved_assets
