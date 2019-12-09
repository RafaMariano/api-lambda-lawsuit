import unittest
import requests
from bs4 import BeautifulSoup

from src import lambda_aws


class TestRequest(unittest.TestCase):
    PATH_HTML = None
    API_ENDPOINT = None
    API_KEY = None

    @classmethod
    def setUpClass(cls):
        with open(cls.PATH_HTML, "rb") as html_file:
            b_html = html_file.read()

        cls.b_html = b_html
        cls.request_aws = requests.post(url=cls.API_ENDPOINT, data=b_html, headers={'x-api-key': cls.API_KEY,
                                                                                    'Content-Type': 'text/html'}).json()

    def test_get_process_data(self):
        json_process_data = lambda_aws.get_process_data(BeautifulSoup(self.b_html, features="html.parser"))
        self.assertEqual(json_process_data, self.request_aws['data']['process_data'])

    def test_process_parts(self):
        json_process_parts = lambda_aws.get_process_parts(BeautifulSoup(self.b_html, features="html.parser"))
        self.assertEqual(json_process_parts, self.request_aws['data']['process_parts'])

    def test_last_movement(self):
        json_last_movement = lambda_aws.get_last_move(BeautifulSoup(self.b_html, features="html.parser"))
        self.assertEqual(json_last_movement, self.request_aws['data']['last_movement'])


if __name__ == '__main__':

    TestRequest.API_ENDPOINT = "https://ij3hepb6ck.execute-api.sa-east-1.amazonaws.com/v2/save-html"
    TestRequest.API_KEY = "API_KEY_HERE"

    for PATH_HTML in ["../data/processo1.html", "../data/processo2.html", "../data/processo3.html"]:
        TestRequest.PATH_HTML = PATH_HTML
        unittest.main()
