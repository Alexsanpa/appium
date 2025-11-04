import time
import unittest
import os

from sapyautomation.desktop.process import launch_process, kill_process

try:
    from sapyautomation.core.com import ComDispatch, ComObject
    from sapyautomation.core.utils.exceptions import InvalidComException
except ImportError:
    pass


class TestComInterface(unittest.TestCase):
    sap_exe = "saplogon.exe"
    sap_path = 'C:\\Program Files (x86)\\SAP\\FrontEnd\\SAPgui'
    sap_name = "SAPGUI"

    def setUp(self) -> None:
        skip = os.environ.get('IGNORE_TESTS', False)
        if skip:
            self.skipTest('Ignore tests variable enable')

    def test_create_invalid_object(self):
        self.assertRaises(InvalidComException, ComObject, "gg")

    def test_create_invalid_dispatch(self):
        self.assertRaises(InvalidComException, ComDispatch, "gg")

    def test_create_dispatch(self):
        import win32com.client
        sap_gui = ComDispatch("WScript.Shell").get()
        self.assertEqual(win32com.client.CDispatch, type(sap_gui))

    def test_create_object(self):
        import win32com.client
        launch_process(self.sap_path + "\\" + self.sap_exe)
        time.sleep(1)
        sap_gui = ComObject().get()
        self.assertEqual(type(sap_gui), win32com.client.CDispatch)
        kill_process(self.sap_exe)
