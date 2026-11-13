from cart import calculate_total

cases = [
    ({"사과": (1000, 2)}, 2000),
    ({"사과": (1000, 3)}, 2550),
    ({}, 0),
    ({"사과": (1000, 2), "배": (1500, 4)}, 7100),
    ({"우유": (1250, 3)}, 3188),
]

passed = 0
for i, (data, want) in enumerate(cases, 1):
    got = calculate_total(data)
    passed += (got == want)
    print(i, '기대', want, '실제', got)
print('통과', passed, '/ 5')