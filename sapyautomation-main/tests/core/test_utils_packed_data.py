import os
import unittest
import pathlib
from sapyautomation.core.utils.general import PackedData


class TestSettingsCases(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path = pathlib.Path.cwd()
        cls.settings_file = path.joinpath('settings.ini')

        with open(cls.settings_file, 'w+') as fh:
            fh.writelines(['[ENV]\n', 'CUSTOM_SETTINGS_ENABLED = false'])

        os.environ['SAPY_SETTINGS'] = str(cls.settings_file)

        cls.packed_data = PackedData('test')

    def test_append_data(self):
        self.packed_data.append('A', 'a')
        self.packed_data.append('B', 'b')
        self.assertEqual(self.packed_data.get('A'), 'a')
        self.assertEqual(self.packed_data.get('B'), 'b')

    def test_replace_data(self):
        self.packed_data.append('C', 'a')
        self.packed_data.replace('C', 'C')
        self.assertNotEqual(self.packed_data.get('C'), 'a')

    def test_delete_data(self):
        self.packed_data.append('D', 'a')
        self.assertEqual(self.packed_data.get('D'), 'a')
        self.packed_data.remove('D')

        self.assertEqual(self.packed_data.get('D'), None)

    def test_file_serialization(self):
        self.packed_data.append('E', 'e')
        self.packed_data.append('F', 5)

        old_data = self.packed_data._data

        self.packed_data.saveToFile()
        self.packed_data.readFromFile()

        self.assertEqual(self.packed_data._data, old_data)

    @classmethod
    def tearDownClass(cls):
        cls.settings_file.unlink()


if __name__ == '__main__':
    unittest.main()
