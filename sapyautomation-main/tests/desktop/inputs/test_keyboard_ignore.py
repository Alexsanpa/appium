import os
import ctypes
import unittest


class TestKeyboardCases(unittest.TestCase):

    def setUp(self):
        self.skip = os.environ.get('IGNORE_TESTS', False)
        if self.skip:
            self.skipTest('Ignore tests variable enable')

    def test_caps_lock(self):
        from win32con import VK_CAPITAL
        from sapyautomation.desktop.inputs.keyboard import caps_lock
        caps_lock()
        hllDll = ctypes.WinDLL("User32.dll")
        is_caps_lock = hllDll.GetKeyState(VK_CAPITAL)
        caps_lock()
        self.assertTrue(is_caps_lock)

    def test_num_lock(self):
        from win32con import VK_NUMLOCK
        from sapyautomation.desktop.inputs.keyboard import num_lock
        num_lock()
        hll_dll = ctypes.WinDLL("User32.dll")
        is_num_lock = hll_dll.GetKeyState(VK_NUMLOCK)
        if not is_num_lock:
            num_lock()
            is_num_lock = hll_dll.GetKeyState(VK_NUMLOCK)

        num_lock()
        self.assertTrue(is_num_lock)

    def test_press_key(self):
        from sapyautomation.desktop.inputs.keyboard import press_key, enter
        press_key("w")
        enter()
        self.assertTrue(input() == "w")
        self.assertRaises(KeyError, press_key, "Hello")

    def test_type_text(self):
        from sapyautomation.desktop.inputs.keyboard import type_text, enter
        type_text("testing:")
        enter()
        self.assertTrue(input() == "testing:")
        self.assertRaises(KeyError, type_text, "Hel♥lo")

    def test_hot_key(self):
        from sapyautomation.desktop.inputs.keyboard import press_hot_key
        self.assertRaises(KeyError, press_hot_key, "ctrl", "fake")
        self.assertRaises(KeyError, press_hot_key, "ctrl", "alt", "fake")
        self.assertTrue(KeyError, press_hot_key("ctrl", "alt"))

    def test_spacebar_backspace_delete_end_key(self):
        from sapyautomation.desktop.inputs.keyboard import type_text, \
            space_bar, home_key, delete, end_key, backspace, enter
        type_text("hello")
        space_bar()
        type_text("world")
        home_key()
        delete()
        end_key()
        backspace()
        enter()
        self.assertTrue(input() == "ello worl")
