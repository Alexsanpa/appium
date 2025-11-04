import datetime

from sapyautomation.core.utils.general import wait


class TestGeneral:

    def test_wait(self):
        wait_time = 5

        start = datetime.datetime.now()
        wait(wait_time)
        delta = datetime.datetime.now() - start

        assert delta.seconds == wait_time
