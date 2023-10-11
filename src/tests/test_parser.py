import unittest
from bs4 import BeautifulSoup
from lib.parser import extract_links, extract_images, extract_metadata, get_asset_urls


class TestParser(unittest.TestCase):

    def setUp(self):
        # Sample HTML content for testing
        self.sample_html = """
        <html>
            <head>
                <title>Test Page</title>
            </head>
            <body>
                <a href="https://www.example1.com">Link 1</a>
                <a href="https://www.example2.com">Link 2</a>
                <img src="image1.jpg" alt="Image 1">
                <img src="image2.jpg" alt="Image 2">
            </body>
        </html>
        """
        self.soup = BeautifulSoup(self.sample_html, 'html.parser')

    def test_when_extract_links_then_correct_number_returned(self):
        links = extract_links(self.soup)
        self.assertEqual(len(links), 2)
        self.assertIn("https://www.example1.com", links)
        self.assertIn("https://www.example2.com", links)

    def test_when_extract_images_then_correct_number_returned(self):
        images = extract_images(self.soup)
        self.assertEqual(len(images), 2)
        self.assertIn("image1.jpg", images)
        self.assertIn("image2.jpg", images)

    def test_when_extract_metadata_then_correct_data_returned(self):
        metadata = extract_metadata(self.sample_html)
        self.assertEqual(metadata['num_links'], 2)
        self.assertEqual(metadata['num_images'], 2)

    def test_when_get_asset_urls_then_correct_urls_returned(self):
        asset_urls = get_asset_urls(self.sample_html, "http://localhost:8080/")
        self.assertEqual(len(asset_urls), 2)
        self.assertIn("http://localhost:8080/image1.jpg", asset_urls.values())
        self.assertIn("http://localhost:8080/image2.jpg", asset_urls.values())

    def test_when_extract_last_fetch_then_correct_format_returned(self):
        metadata = extract_metadata(self.sample_html)
        self.assertTrue("UTC" in metadata['last_fetch'])


if __name__ == '__main__':
    unittest.main()
