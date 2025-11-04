import os
import unittest
try:
    from sapyautomation.vendors.sap.connection import SAP
    from sapyautomation.vendors.sap.login import Login
    from sapyautomation.vendors.sap.start_transaction import create_new_mode
    from sapyautomation.vendors.sap.start_transaction import start_transaction
    from sapyautomation.vendors.sap.start_transaction import click_exit_system
except ImportError:
    pass


class Test_tool_bar(unittest.TestCase):
    def setUp(self) -> None:
        skip = os.environ.get('IGNORE_TESTS', False)
        if skip:
            self.skipTest('Ignore tests variable enable')

        sap = SAP("AMCO DEV")
        sap.start()
        login = Login()
        system = login.identify_system(0)

        if system == "E5G":
            self.assertEqual((login.login(client="100",
                                          user=os.environ.get('E5G_USER'),
                                          password=os.environ.get(
                                              'E5G_PASSWORD'),
                                          language="ES")), "SAP Easy Access")
        elif system == "SDC":
            self.assertEqual((login.login(client="110",
                                          user=os.environ.get('SDC_USER'),
                                          password=os.environ.get(
                                              'SDC_PASSWORD'),
                                          language="ES")),
                             "SAP Easy Access")

    def test_click_exit_system(self):
        create_new_mode(0)
        create_new_mode(0)
        create_new_mode(0)
        self.assertEqual(click_exit_system(0), True)

    def test_create_new_mode(self):
        self.assertEqual(create_new_mode(0), True)
        SAP.close()

    def test_create_new_mode_fail(self):
        create_new_mode(0)
        create_new_mode(0)
        create_new_mode(0)
        create_new_mode(0)
        create_new_mode(0)
        self.assertRaises(SystemError, create_new_mode, 0)
        SAP.close()

    def test_start_transaction(self):
        self.assertEqual(start_transaction(0, "SE11"), True)
        SAP.close()

    def test_start_transaction_without_authorization(self):
        self.assertRaises(ValueError, start_transaction, 0, "AL08")
        SAP.close()

    def test_start_transaction_not_exists(self):
        self.assertRaises(ValueError, start_transaction, 0, "FHC")
        SAP.close()

    def test_start_transaction_option_incorrect(self):
        self.assertRaises(ValueError, start_transaction, 0, "SE37",
                          "/x")
        SAP.close()

    def test_start_transaction_session_not_created(self):
        create_new_mode(0)
        create_new_mode(0)
        create_new_mode(0)
        create_new_mode(0)
        create_new_mode(0)
        self.assertRaises(SystemError, start_transaction, 0,
                          "SE11", "/o")
        SAP.close()
