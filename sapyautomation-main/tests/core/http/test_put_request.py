import unittest

from sapyautomation.core import http


class TestPutRequest(unittest.TestCase):
    def setUp(self) -> None:
        self.skipTest('Ignore tests variable enable')

    @classmethod
    def setUpClass(cls):
        cls.put_ob = http
        cls.url = "https://webhook.site/338789e3-1eca-40ba-8281-0d5fa9999379"
        cls.payload = "{ \n\t\"name\": \"Luis\",\n\t\"password\":" \
                      " \"1234\",\n\t\"auth\": \"admin\"\n\t\n }"

    @unittest.skip
    def test_put_request_no_header(self):
        r = self.put_ob.put_request(self.url, self.payload)
        self.assertEqual(r.status_code, 200)


if __name__ == '__main__':
    unittest.main()
