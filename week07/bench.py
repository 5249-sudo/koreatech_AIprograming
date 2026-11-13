import paths as p

assert p.min_coins_greedy([1, 3, 4], 6) == 3
assert p.min_coins_dp([1, 3, 4], 6) == 2
assert p.min_coins_dp([2, 4], 3) == -1
assert p.min_coins_dp([], 0) == 0
print("거스름돈검증통과: 그리디 3개 / DP 2개")

from graphs import campus
from copy import deepcopy

expected = {'A': 0, 'B': 10, 'C': 22, 'D': 15,
            'E': 8, 'F': 13, 'G': 17, 'H': 16}
for fn in [p.dijkstra_array, p.dijkstra_heap]:
    original = deepcopy(campus)
    dist, prev = fn(campus, 'A')
    assert dist == expected
    path = p.build_path(prev, 'A', 'G')
    assert path == ['A', 'E', 'F', 'G']
    assert campus == original
    print(fn.__name__, dist['G'], path, "검증통과")


for fn in [p.dijkstra_array, p.dijkstra_heap]:
    dist, prev = fn({'A': [], 'B': []}, 'A')
    assert dist['B'] == float('inf')
    assert prev['B'] is None
    assert p.build_path(prev, 'A', 'B') == []
    assert p.build_path(prev, 'A', 'A') == ['A']

print("도달불가·자기경로검증통과")


neg = {'A': [('B', 2), ('C', 3)],
       'B': [], 'C': [('B', -2)]}
for fn in [p.dijkstra_array, p.dijkstra_heap]:
    try:
        fn(neg, 'A')
    except ValueError:
        print(fn.__name__, "음수입력거부확인") 
    else:
        raise AssertionError("음수가중치검사필요")

import paths as p
from graphs import make_graph
from measure import measure

for v in [100, 300, 1000, 3000, 10000]:
    g = make_graph(v, degree=6)
    t1 = measure(lambda x: p.dijkstra_array(x, 0), g)
    t2 = measure(lambda x: p.dijkstra_heap(x, 0), g)
    print(
        v,
        round(t1 * 1000, 2), 
        round(t2 * 1000, 2), 
        round(t1 / t2, 1)
    )
    