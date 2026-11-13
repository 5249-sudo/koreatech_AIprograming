scores_a = {"민수": 85, "지훈": 55, "서연": 92}
scores_b = {"하늘": 78, "준호": 45, "지민": 88}
# A반처리
total = 0
for name in scores_a:
    total = total + scores_a[name]
avg_a = total / len(scores_a)
print("=" * 30)
print("A반결과")
print("=" * 30)
passed = 0
for name in scores_a:
    if scores_a[name] >= 60:
        passed = passed + 1
print("평균:", round(avg_a, 1))
print("합격자수:", passed)

# B반처리
total = 0
for name in scores_b:
    total = total + scores_b[name]
avg_b = total / len(scores_b)
print("=" * 30)
print("B반결과")
print("=" * 30)
passed = 0
for name in scores_b:
    if scores_b[name] >= 60:
        passed = passed + 1
print("평균:", round(avg_b, 1))
print("합격자수:", passed)