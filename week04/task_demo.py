def count_passed(grades):
    """
    grades는 학생 이름(str)을 키, 점수(int)를 값으로 갖는 딕셔너리입니다.
    점수가 60 이상인 학생의 수를 정수로 반환합니다.
    60점은 합격에 포함합니다.
    빈 딕셔너리가 들어오면 0을 반환합니다.
    """
    return sum(score >= 60 for score in grades.values())

cases = [
    {"민수": 85, "지훈": 55}, {"A": 59}, {"A": 60},
    {"A": 90, "B": 95}, {"A": 10, "B": 20}, {}
]
for grades in cases:
    result = count_passed(grades)
    print(grades, repr(result), type(result).__name__)

