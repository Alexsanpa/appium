import os
import unittest

try:
    from sapyautomation.vendors.sap.connection import SAP
    from sapyautomation.vendors.sap.login import Login
except ImportError:
    pass


class TestLogin(unittest.TestCase):

    def setUp(self) -> None:
        skip = os.environ.get('IGNORE_TESTS', False)
        if skip:
            self.skipTest('Ignore tests variable enable')
        sap = SAP("AMCO DEV")
        sap.start()

    def test_login(self):
        login = Login()
        system = login.identify_system(0)

        if system == "E5G":
            self.assertEqual((login.login(client="100", user="ROGARCIA",
                                          password="Mfc22.bull",
                                          language="ES")), "SAP Easy Access")
        elif system == "SDC":
            self.assertEqual((login.login(client="110", user="HCHAIREZ",
                                          password="Deloitte.01",
                                          language="ES")),
                             "SAP Easy Access")

    def test_logincce_fail(self):
        login = Login()
        system = login.identify_system(0)
        if system == "E5G":
            self.assertRaises(ConnectionError,
                              login.login(client="110", user="ROGARCIA",
                                          password="Mfc22.bull",
                                          language="ES"))
        elif system == "SDC":
            self.assertRaises(ConnectionError, login.login, client="110",
                              user="HCHAIREZ", password="Deloitte.00",
                              language="ES")

    def tearDown(self) -> None:
        sap = SAP("AMCO DEV")
        sap.close()
