import algorithms as alg
import random
import time
FUNCS = [alg.bubble_sort, alg.cocktail_sort, alg.insertion_sort,
         alg.patience_sort, alg.pancake_sort]

# 1. 정렬 결과와 원본 보존 검사
for fn in FUNCS:
    for case in [[], [7], [5, 5, 5], [3, 2, 1], [3, 1, 3, 2]]:
        original = case[:]
        assert fn(case) == sorted(original), "정렬 결과 오류"
        assert case == original, "원본 변경"

# 2. 실행시간을 측정하는 함수
def measure(func, data, repeat=5):
    times = []
    for _ in range(repeat):
        copied = data[:]
        start = time.perf_counter()
        func(copied)
        elapsed = time.perf_counter() - start
        times.append(elapsed)
    return min(times)

# 3. 입력 크기별 실행시간 측정
random.seed(6)
SIZES = [1000, 2000, 5000, 10000]

for n in SIZES:
    data = [random.randint(1, 100000) for _ in range(n)]
    row = [str(n)]

    for fn in FUNCS + [sorted]:
        row.append(f"{measure(fn, data):.6f}")
    print("\t".join(row))


n = 5000
base = [random.randint(1, 100000) for _ in range(n)]
INPUTS = {
    "무작위": base,
    "이미정렬": sorted(base),
    "역순": sorted(base, reverse=True),
    "중복많음": [random.randint(1, 10) for _ in range(n)],
}
for label, data in INPUTS.items():
    print(label, [f"{measure(fn, data):.4f}" for fn in FUNCS])


print("\n[중복찾기: 개선전실행시간]")

for n in [2000, 5000, 10000]:
    items = [random.randint(1, n // 2) for _ in range(n)]
    elapsed = measure(alg.find_duplicates, items)
    print(n, f"{elapsed:.6f}", "초")

before, after = alg.find_duplicates, alg.find_duplicates_fast

for case in [[], [7], [5, 5, 5], [2, 1, 1, 2]]:
    assert before(case) == after(case), "값 또는 순서 불일치"

for n in [2000, 5000, 10000]:
    items = [random.randint(1, n // 2) for _ in range(n)]
    assert before(items) == after(items), "값 또는 순서 불일치"
    t1 = measure(before, items)
    t2 = measure(after, items)
    print(n, f"{t1:.4f}", f"{t2:.6f}", f"{t1 / t2:.1f}배", "일치")