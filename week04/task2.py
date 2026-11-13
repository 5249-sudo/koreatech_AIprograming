def to_grade(score):
    """
    입력: 정수 score (0~100 범위)
    처리:- 0 미만 또는 100 초과 → "invalid"
        - 90~100 → "A"
        - 80~89 → "B"
        - 70~79 → "C"
        - 60~69 → "D"
        - 0~59 → "F"
    출력: 학점 문자열(str)
    경계: score < 0 또는 score > 100 → "invalid"
    """
    if score < 0 or score > 100:
        return "invalid"
    elif score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    else:
        return "F"

scores = [-1, 0, 59, 60, 69, 70, 75, 79, 80, 89, 90, 100, 101]
for score in scores:
    result = to_grade(score)
    print(score, repr(result), type(result).__name__)
