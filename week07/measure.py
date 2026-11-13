import time
from copy import deepcopy  # 추가

def measure(func, data, repeat=5):
    times = []

    for _ in range(repeat):
        copied = deepcopy(data)  # data[:]에서변경
        start = time.perf_counter()
        func(copied)
        elapsed = time.perf_counter() - start
        times.append(elapsed)

    return min(times)
