import os
import unittest

from sapyautomation.core.utils.exceptions import SapSessionNotFound

try:
    from sapyautomation.vendors.sap.connection import SAP
    from sapyautomation.vendors.sap.login import Login
except ImportError:
    pass


class TestGeneralMethods(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.skip = os.environ.get('IGNORE_TESTS', False)

        if not cls.skip:
            cls.sap = SAP("S4 INICIATIVA")
            cls.sap.start()
            login = Login()
            login.identify_system(0)
            login.login(
                client=100,
                user=os.environ.get('S4M_USER'),
                password=os.environ.get('S4M_PASSWORD'),
                language="ES")

    def setUp(self) -> None:
        if self.skip:
            self.skipTest('Ignore tests variable enable')

    def test_get_sap_information(self):
        sap_information = SAP.get_sap_information()
        self.assertEqual("USSLTCSNL1353", sap_information.application_server)
        self.assertEqual("S4M", sap_information.system_name)
        self.assertEqual(0, sap_information.system_number)
        self.assertEqual("ES", sap_information.language)
        self.assertEqual("100", sap_information.client)
        self.assertEqual(1, sap_information.session)
        self.assertEqual("", sap_information.group)
        self.assertEqual("SAPLSMTR_NAVIGATION", sap_information.program)
        self.assertIsInstance(sap_information.response_time, int)

    def test_get_sap_information_raises(self):
        self.assertRaises(SapSessionNotFound, SAP.get_sap_information, 5)

    @classmethod
    def tearDownClass(cls) -> None:
        if not cls.skip:
            cls.sap.close()
