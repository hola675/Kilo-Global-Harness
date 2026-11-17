from calculator import divide, percentage


def test_divide_positive_numbers():
    assert divide(8, 2) == 4


def test_percentage_regular_case():
    assert percentage(25, 100) == 25
