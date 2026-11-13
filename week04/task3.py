def top_student(grades):
    """
    입력: 학생 이름(str)을 키, 점수(int)를 값으로 갖는 딕셔너리 grades
    처리: 최고 점수를 찾는다
         동점이면 이름을 사전순으로 비교해 앞선 학생을 고른다
    출력: 최고점 학생 이름(str)
    경계: 빈 딕셔너리 {}가 입력되면 None을 반환한다
    """
    if not grades:
        return None

    max_score = max(grades.values())
    top_students = [name for name, score in grades.items() if score == max_score]
    return min(top_students)
cases = [
    {"A": 80, "B": 95, "C": 90},
    {"B": 90, "A": 90, "C": 80},
    {"A": 90, "B": 90, "C": 80}, {"A": 75}, {}
]
for grades in cases:
    result = top_student(grades)
    print(grades, repr(result), type(result).__name__)
