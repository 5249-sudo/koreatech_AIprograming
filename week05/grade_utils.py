def calculate_average(scores):
    total = 0
    for name in scores:
        total = total + scores[name]
    return total / len(scores)


def count_passed(scores, cutoff=60):
    passed = 0
    for name in scores:
        if scores[name] >= cutoff:
            passed = passed + 1
    return passed


def print_header(title):
    """title(str)을 구분선과 함께 화면에 출력합니다. 반환값은 없습니다."""
    print("=" * 30)
    print(title)
    print("=" * 30)


def report(title, scores):
    """한 반의 결과를 화면에 출력합니다."""
    print_header(title)
    print("평균:", round(calculate_average(scores), 1))
    print("합격자수:", count_passed(scores))