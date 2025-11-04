from sapyautomation.core.test_cases import BaseTestCases


class XTestCase(BaseTestCases):
    pass


class TestNewTutu(XTestCase):

    def test_dos(self):
        self.step_a()

    def step_a(self):
        pass
