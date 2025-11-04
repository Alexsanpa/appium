import unittest

from sapyautomation.core import http


class TestGetRequest(unittest.TestCase):
    def setUp(self) -> None:
        self.skipTest('Ignore tests variable enable')

    @classmethod
    def setUpClass(cls):
        cls.get_ob = http
        cls.url = "https://webhook.site/338789e3-1eca-40ba-8281-0d5fa9999379"
        cls.wrong_url = "https://www.transfermarkt.com/jumplist/startseite" \
                        "/wettbewerb/GB1"
        cls.header = 'Server'

    @unittest.skip
    def test_get_200(self):
        r = self.get_ob.get_request(self.url)
        self.assertEqual(r.status_code, 200)

    @unittest.skip
    def test_get_404(self):
        r = self.get_ob.get_request(self.wrong_url)
        self.assertIsNot(r.status_code, 404)

    @unittest.skip
    def test_is_not_none(self):
        r = self.get_ob.get_request(self.url)
        self.assertIsNot(r.status_code, None)

    @unittest.skip
    def test_url_not_valid(self):
        not_an_url = "https://asdfasdfas.com"
        self.assertRaises(Exception, self.get_ob.get_request, not_an_url)

    @unittest.skip
    def test_get_header(self):
        r = self.get_ob.get_request(self.url, headers=self.header)
        self.assertEqual(r.status_code, 200)


if __name__ == '__main__':
    unittest.main()
