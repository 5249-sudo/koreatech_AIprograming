# bug5_missing.py  —  ⑤ 요구사항 누락
# ---------------------------------------------------------------------------
# 상황
#   AI에게 spec5.txt 의 명세를 주고 받은 코드입니다.
#   실행하면 오류가 하나도 나지 않고, 답도 전부 그럴듯합니다.
#   그런데 명세와 대조해 보면 세 칸이 통째로 구현되어 있지 않습니다.
#
# 할 일 (20분)
#   1. spec5.txt 를 먼저 읽는다.
#   2. 여섯 칸 옆에 [구현됨 / 누락됨 / 확인불가] 를 적어 대조표를 만든다.
#   3. 누락 세 건을 찾아 기록지 ①③에 적는다.
#   4. 고친 뒤 test_fixed.py 로 회귀 검증한다.
#
# 그리고 except: 가 왜 금물인가
#   아래의 bare except 는 모든 예외를 삼킵니다.
#   빈 리스트의 ZeroDivisionError 도,
#   오타로 생긴 NameError 도,
#   숫자가 아닌 값의 TypeError 도
#   전부 조용히 "F" 가 되어 버립니다.
#   → 오류를 없애는 것과 오류를 안 보이게 하는 것은 다릅니다.
#     고칠 때는 except: 를 지우고 필요한 예외만 골라 잡거나,
#     애초에 if not scores: 로 먼저 걸러 내세요.
# ---------------------------------------------------------------------------

def grade(scores):
    if not scores:
        return "측정불가"

    if any(score < 0 or score > 100 for score in scores):
        raise ValueError("점수는 0 이상 100 이하이어야 합니다")

    avg = round(sum(scores) / len(scores), 1)

    if avg >= 90:
        return "A"
    elif avg >= 80:
        return "B"
    elif avg >= 70:
        return "C"
    elif avg >= 60:
        return "D"
    else:
        return "F"


print(grade([]))            # '측정불가' 여야 하는데?
print(grade([89, 90, 90]))  # 평균 89.67 → ⑥ 반올림하면 90 → 'A' 여야 하는데?

# 아래 한 줄은 명세 ⑤ 를 확인하기 위한 것입니다.
# 제대로 고치고 나면 여기서 ValueError 가 나는 것이 "정상"입니다.
# 그 상태가 되면 이 줄 앞에 # 을 붙여 주석 처리한 뒤 test_fixed.py 를 실행하세요.
# print(grade([120, 130]))    # ValueError 여야 하는데?
