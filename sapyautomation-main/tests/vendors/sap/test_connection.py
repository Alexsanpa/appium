import os
import unittest

try:
    from sapyautomation.vendors.sap.connection import SAP
except ImportError:
    pass


class TestConnection(unittest.TestCase):
    session = None

    def setUp(self) -> None:
        skip = os.environ.get('IGNORE_TESTS', False)
        if skip:
            self.skipTest('Ignore tests variable enable')

    def test_connection(self):
        sap = SAP('AMCO DEV')
        self.session = sap.start()
        self.assertEqual(self.session.findByID("wnd[0]/titl").text, "SAP")
        sap.close_windows()
        SAP.close()

    def test_connection_fail(self):
        sap = SAP("Test")
        self.assertRaises(ConnectionError, sap.start)
        SAP.close()

    def test_assert_connection_name(self):
        self.assertRaises(AssertionError, SAP, connection_name='')

    def test_file_not_found(self):
        sap = SAP("Sandbox", path="C:\\Program Files ("
                                  "x86)\\SAP\\FrontEnd1\\SAPgui\\saplogon.exe")

        self.assertRaises(FileNotFoundError, sap.start)

    def test_wait_implicit(self):
        sap = SAP("AMCO DEV",
                  path="C:\\Program Files ("
                       "x86)\\SAP\\FrontEnd\\SAPgui\\saplogon.exe",
                  time=.001)
        self.assertRaises(SystemError, sap.start)
        sap.close()

    def test_close(self):
        sap = SAP("AMCO DEV")
        self.session = sap.start()
        self.assertEqual(sap.close(), True)

    def test_close_windows(self):
        sap = SAP("AMCO DEV")
        sap.start()
        self.assertEqual(sap.close_windows(), True)
