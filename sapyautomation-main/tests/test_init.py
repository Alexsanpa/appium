from sapyautomation.app import new_array


def test_case_new_array():
    array = new_array(10)
    assert len(array)
