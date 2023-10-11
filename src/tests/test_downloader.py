import unittest
import os
import logging
import responses
from requests.exceptions import ConnectionError
from lib.downloader import download_page, download_assets

logging.disable(logging.CRITICAL)


class TestDownloader(unittest.TestCase):

    def setUp(self):
        self.sample_url = "http://localhost:8080"
        self.output_path = os.path.join("output", "localhost:8080")
        self.sample_asset_url = "http://localhost:8080/image.jpg"

    def tearDown(self):
        index_html_path = os.path.join(self.output_path, "index.html")
        image_jpg_path = os.path.join(self.output_path, "image.jpg")
        if os.path.exists(index_html_path):
            os.remove(index_html_path)
        if os.path.exists(image_jpg_path):
            os.remove(image_jpg_path)

    @responses.activate
    def test_when_download_page_then_file_saved(self):
        responses.add(responses.GET, self.sample_url, body="fake_html_content", status=200)
        download_page(self.sample_url, self.output_path)
        self.assertTrue(os.path.exists(os.path.join(self.output_path, "index.html")))

    @responses.activate
    def test_when_download_asset_then_file_saved(self):
        responses.add(responses.GET, self.sample_asset_url, body="fake_image_content", status=200)
        download_assets({self.sample_asset_url: self.sample_asset_url}, self.output_path)
        self.assertTrue(os.path.exists(os.path.join(self.output_path, "image.jpg")))

    @responses.activate
    def test_when_non_200_response_then_no_file_saved(self):
        responses.add(responses.GET, self.sample_url, body="Not Found", status=404)
        result = download_page(self.sample_url, self.output_path)
        self.assertIsNone(result)

    @responses.activate
    def test_when_network_error_then_no_file_saved(self):
        responses.add(responses.GET, self.sample_url, body=ConnectionError('Network Error'))
        result = download_page(self.sample_url, self.output_path)
        self.assertIsNone(result)

    @responses.activate
    def test_when_some_assets_fail_then_only_success_saved(self):
        responses.add(responses.GET, self.sample_asset_url, body="fake_image_content", status=200)
        responses.add(responses.GET, "http://localhost:8080/image2.jpg", body=ConnectionError('Network Error'))
        assets = download_assets({
            self.sample_asset_url: self.sample_asset_url,
            "http://localhost:8080/image2.jpg": "image2.jpg"
        }, self.output_path)
        self.assertEqual(len(assets), 1)


if __name__ == '__main__':
    unittest.main()
