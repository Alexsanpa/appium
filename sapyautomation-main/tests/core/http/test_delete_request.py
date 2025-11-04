import unittest

from sapyautomation.core import http


class TestDeleteRequest(unittest.TestCase):
    def setUp(self) -> None:
        self.skipTest('Ignore tests variable enable')

    @classmethod
    def setUpClass(cls):
        cls.delete_ob = http
        cls.url = "https://webhook.site/338789e3-1eca-40ba-8281-0d5fa9999379"
        cls.not_an_url = "https://asdfasdfl.com"
        cls.payload = "{ \n\t\"name\": \"Luis\",\n\t\"password\": \"1234\"" \
                      ",\n\t\"auth\": \"admin\"\n\t\n }"
        cls.headers = {
            'Content-Type': 'application/json'
        }

    @unittest.skip
    def test_delete_request_no_header(self):
        r = self.delete_ob.delete_request(self.url, self.payload)
        self.assertEqual(r.status_code, 200)

    @unittest.skip
    def test_delete_request_headers(self):
        r = self.delete_ob.delete_request(
            self.url, self.payload, self.headers)
        self.assertEqual(r.status_code, 200)

    @unittest.skip
    def test_post_failure_web_page(self):
        self.assertRaises(Exception, self.delete_ob.delete_request,
                          self.not_an_url)


if __name__ == '__main__':
    unittest.main()
