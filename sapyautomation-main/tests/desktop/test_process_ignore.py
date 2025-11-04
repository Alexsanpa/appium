import os
import time
import unittest
from sapyautomation.desktop.process import launch_process, \
    is_process_running, kill_process, list_running_processes, \
    is_chrome_running, is_firefox_running, is_edge_running, \
    open_program_by_name, is_sap_running

try:
    from sapyautomation.vendors.sap.connection import SAP
except ImportError:
    pass


class TestProcessCases(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.process = "C:\\Program Files (" \
                      "x86)\\SAP\\FrontEnd\\SAPgui\\saplogon.exe"
        cls.process_name = "saplogon.exe"
        cls.fake_process = "C:\\Program Files (" \
                           "x86)\\SAP\\FrontEnd\\SAPgui\\gg.ezxe"
        cls.browser = "firefox"

    def setUp(self):
        skip = os.environ.get('IGNORE_TESTS', False)
        if skip:
            self.skipTest('Ignore tests variable enable')

    def test_launch_process(self):
        launch_process(self.process)
        self.assertTrue(is_process_running(self.process_name))
        self.assertRaises(FileNotFoundError, launch_process,
                          self.process_name + "name")
        kill_process(self.process_name)

        launch_process(self.browser)
        self.assertTrue(is_process_running(self.browser))
        self.assertRaises(FileNotFoundError, launch_process, self.fake_process)
        kill_process(self.browser)

    def test_is_process_running(self):
        launch_process(self.process)
        self.assertTrue(is_process_running(self.process_name))
        kill_process(self.process_name)
        self.assertFalse(is_process_running(self.process_name))

    def test_open_program_by_name(self):
        self.assertRaises(FileNotFoundError, open_program_by_name,
                          "fakeProcess", os.path.dirname(__file__))
        open_program_by_name(self.process_name, self.process.replace(
            self.process_name, ''))
        self.assertTrue(is_process_running(self.process_name))
        kill_process(self.process_name)

    def test_kill_process(self):
        process = launch_process(self.process)
        self.assertTrue(is_process_running(process))
        kill_process(process_name=process)
        self.assertRaises(FileNotFoundError, kill_process, self.fake_process)
        self.assertRaises(FileNotFoundError, kill_process, "fakeProcess")
        self.assertRaises(FileNotFoundError, kill_process, True)
        self.assertRaises(FileNotFoundError, kill_process, "fake p")
        self.assertRaises(ValueError, kill_process, None,
                          "fake Process?")
        self.assertFalse(is_process_running(process))

    def test_list_running_processes(self):
        lista = list_running_processes()
        self.assertIsInstance(lista, set)
        self.assertTrue(lista)

    @unittest.skip("edge closes just after is opened")
    def test_is_edge_running(self):
        exe = "microsoftedge"
        pro = launch_process(exe)
        time.sleep(2)
        self.assertTrue(is_edge_running())
        kill_process(pro)
        self.assertFalse(is_edge_running())

    @unittest.skip("chrome in use during testing")
    def test_is_chrome_running(self):
        exe = "chrome"
        launch_process(exe)
        time.sleep(3)
        self.assertTrue(is_chrome_running())
        kill_process(exe)
        time.sleep(2)
        self.assertFalse(is_chrome_running())

    def test_is_firefox_running(self):
        exe = "firefox"
        launch_process(exe)
        time.sleep(1)
        self.assertTrue(is_firefox_running())
        kill_process(exe)
        time.sleep(1)
        self.assertFalse(is_firefox_running())

    def test_is_sap_running(self):
        sap = SAP("AMCO DEV")
        sap.start()
        time.sleep(1)
        self.assertTrue(is_sap_running())
        sap.close()
        time.sleep(1)
        self.assertFalse(is_sap_running())
