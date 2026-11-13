from bug3_logic import find_max


def test_maximum_is_first():
    assert find_max([95, 85, 70, 60]) == 95


def test_maximum_is_in_middle():
    assert find_max([10, 30, 20]) == 30


def test_maximum_is_last():
    assert find_max([70, 85, 60, 95]) == 95


def test_single_item():
    assert find_max([42]) == 42


def test_negative_scores():
    assert find_max([-8, -2, -5]) == -2
