from sapyautomation.core.utils.general import get_resource
from sapyautomation.desktop.files import SpreadSheetData


class TestData:
    """Data ModelClass for tests data with spreadsheet backend

    Args:
        path(str): relative spreadsheet path

    """

    def __init__(self, path: str):
        full_path = get_resource(path)
        self.__book = SpreadSheetData(full_path)

    @property
    def data(self) -> dict:
        """Returns Test data loaded from file"""
        if not hasattr(self, "__data"):
            self.load_data()

        return self.__data

    def load_data(self):
        """Loads test data from spreadsheet file"""
        self.__data = {}

        for sheet in self.__book.get_sheets():
            self.__data[sheet] = {}
            keys = [
                cell.value for cell in self.__book._book[sheet]["A"]
            ]  # Assuming keys are in column 'A'
            values = [
                cell.value for cell in self.__book._book[sheet]["B"]
            ]  # Assuming values are in column 'B'

            for index in range(1, len(keys)):
                self.__data[sheet][keys[index]] = values[index]
