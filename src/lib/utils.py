import os
from urllib.parse import urlparse


def get_output_path(url):
    """Get the output directory for the provided URL."""
    output_dir = os.environ.get("OUTPUT_DIR", "output")
    domain_name = urlparse(url).netloc
    return os.path.join(output_dir, domain_name)


def ensure_url_protocol(url):
    if not url.startswith(('http://', 'https://')):
        return 'https://' + url
    return url
