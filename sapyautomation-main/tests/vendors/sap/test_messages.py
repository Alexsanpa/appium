import os
import unittest


try:
    from sapyautomation.vendors.sap import messages
    from sapyautomation.vendors.sap.connection import SAP
except ImportError:
    pass


class TestMessages(unittest.TestCase):
    def setUp(self) -> None:
        skip = os.environ.get('IGNORE_TESTS', False)
        if skip:
            self.skipTest('Ignore tests variable enable')

        self.sap = SAP("AMCO DEV")
        self.sap.start()

    def test_identify_message(self):
        session = SAP.get_current_connection(0)
        session.findById("wnd[0]").sendVKey(0)
        elements = messages.identify_message(session=session)
        self.assertEqual(elements != '', True)

    def tearDown(self) -> None:
        SAP.close()
