from grade_utils import calculate_average, count_passed

cases = [
    ({"A": 59}, (59.0, 0)),
    ({"A": 60}, (60.0, 1)),
    ({"A": 59, "B": 60}, (59.5, 1)),
]
for scores, expected in cases:
    actual = (
        calculate_average(scores),
        count_passed(scores),
    )
    print(scores, expected, actual, actual == expected)
