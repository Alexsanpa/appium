from tests import BaseTest

from sapyautomation.core import LazySettings
from sapyautomation.core.test_cases import TestData


class TestTestData(BaseTest):
    @classmethod
    def setUpClass(cls):
        LazySettings().EXTRA_RESOURCES_PATH = cls._resources
        cls.data = TestData('test_files/test_data.xlsx')

    def test_object_instances(self):
        self.assertIsInstance(self.data, TestData)
        self.assertIsInstance(self.data.data, dict)

    def test_sheets_by_name(self):
        first = self.data.data['First']
        second = self.data.data['Second']

        self.assertNotEqual(first, second)

    def test_data(self):
        data = self.data.data['First']

        self.assertTrue(data['color'] == 'red')
        self.assertTrue(data['country'] == 'mexico')
        self.assertTrue(data['animal'] == 'dog')
