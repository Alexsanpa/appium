from tests import BaseTest

from sapyautomation.desktop.files import SpreadSheetData


class TestFilesSpreadSheets(BaseTest):

    @classmethod
    def setUpClass(cls):
        cls.csv_file = cls.get_test_resource('test_files/spreadsheet.csv')
        cls.xls_file = cls.get_test_resource('test_files/spreadsheet.xls')
        cls.xlsx_file = cls.get_test_resource('test_files/spreadsheet.xlsx')

    def test_read_xls_file(self):
        book = SpreadSheetData(self.xls_file)
        self.assertIsInstance(book, SpreadSheetData)

    def test_read_xlsx_file(self):
        book = SpreadSheetData(self.xlsx_file)
        self.assertIsInstance(book, SpreadSheetData)

    def test_get_matrix(self):
        book = SpreadSheetData(self.xlsx_file)
        matrix = book.get_matrix()
        custom_matrix = book.get_custom_matrix((0, 3), (5, 5))

        self.assertEqual(book.count_rows(), len(matrix[0]))
        self.assertEqual(book.count_cols(), len(matrix))
        self.assertEqual(book.get_cell_data(2, 3), matrix[2][3])

        self.assertEqual(2, len(custom_matrix[0]))
        self.assertEqual(5, len(custom_matrix))
        self.assertEqual(book.get_cell_data(0, 3), custom_matrix[0][0])
