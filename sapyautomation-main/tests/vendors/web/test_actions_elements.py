import unittest

import os
from sapyautomation.web import find_elements
from sapyautomation.web.start_browser import Browser
from sapyautomation.web import actions


class TestActionsElements(unittest.TestCase):
    driver = None

    def setUp(self) -> None:
        skip = os.environ.get('IGNORE_TESTS', False)
        if skip:
            self.skipTest('Ignore tests variable enable')

        browser = Browser()
        self.driver = browser.start_browser('Firefox',
                                            'http://ussltcsnl1353.solutions'
                                            '.glbsnet.com:8000/sap/bc'
                                            '/ui5_ui5/ui2/ushell/shells'
                                            '/abap/FioriLaunchpad.html?sap'
                                            '-client=100#Shell-home')

    def test_click(self):
        btn_login = find_elements.find_element_by_id(self.driver, "LOGIN_LINK")
        actions.click(btn_login)
        msj = find_elements. \
            find_element_by_xpath(self.driver,
                                  "//label[text()='Indique un usuario']").text

        self.assertEqual(msj, "Indique un usuario")

        self.driver.close()

    def test_input_text(self):
        txt_user = find_elements. \
            find_element_by_id(self.driver, "USERNAME_FIELD-inner")
        actions.input_text_actions(self.driver, txt_user, "mapaz")
        lbl_user = find_elements. \
            find_element_by_id(self.driver, "USERNAME_FIELD-inner")

        self.assertEqual(lbl_user.get_attribute("value"), "mapaz")
        self.driver.close()

    def test_clear_text(self):
        txt_user = find_elements. \
            find_element_by_id(self.driver, "USERNAME_FIELD-inner")
        actions.input_text_actions(self.driver, txt_user, "mapaz")
        actions.clear_text(txt_user)

        lbl_user = find_elements. \
            find_element_by_id(self.driver, "USERNAME_FIELD-inner")

        self.assertEqual(lbl_user.get_attribute("value") == '', True)
        self.driver.close()

    def test_click_actions(self):
        btn_login = find_elements.find_element_by_id(self.driver, "LOGIN_LINK")
        actions.click_actions(self.driver, btn_login)
        msj = find_elements. \
            find_element_by_xpath(self.driver,
                                  "//label[text()='Indique un usuario']").text

        self.assertEqual(msj, "Indique un usuario")

        self.driver.close()
