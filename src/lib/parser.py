from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urljoin


def extract_links(soup):
    """Extract all links from the parsed HTML."""
    return [link.get('href') for link in soup.find_all('a') if link.get('href')]


def extract_images(soup):
    """Extract all image sources from the parsed HTML."""
    return [img.get('src') for img in soup.find_all('img') if img.get('src')]


def extract_metadata(html_content):
    """Extract metadata from the fetched HTML content."""
    soup = BeautifulSoup(html_content, 'html.parser')

    metadata = {
        'num_links': len(extract_links(soup)),
        'num_images': len(extract_images(soup)),
        'last_fetch': datetime.utcnow().strftime('%a %b %d %Y %H:%M UTC')
    }

    return metadata


def get_asset_urls(html_content, base_url):
    """Extract and return full URLs of all assets (images, scripts, styles) in the HTML content."""
    soup = BeautifulSoup(html_content, 'html.parser')
    asset_tags = soup.find_all(['img', 'script', 'link'])

    asset_urls = {}
    for tag in asset_tags:
        if tag.name == 'img':
            src = tag.get('src')
        elif tag.name == 'script':
            src = tag.get('src')
        elif tag.name == 'link' and tag.get('rel', [''])[0] == 'stylesheet':
            src = tag.get('href')
        else:
            src = None

        if src:
            full_url = urljoin(base_url, src)
            asset_urls[src] = full_url

    return asset_urls
