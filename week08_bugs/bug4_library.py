# bug4_library.py  —  ④ 라이브러리 오류
# ---------------------------------------------------------------------------
# 상황
#   AI가 알려준 대로 그대로 옮겨 적었는데 import 부터 안 됩니다.
#   그리고 그것을 고쳐도 또 다른 곳에서 막힙니다. 잘못된 곳이 세 군데입니다.
#
# 할 일 (15분)  —  30초 확인 절차를 그대로 따라가세요
#   ① 패키지가 실제로 존재하는가
#        PyPI(https://pypi.org) 에서 이름을 검색한다.
#        최근 릴리스 날짜와 소스 저장소 링크가 없으면 설치하지 않는다.
#   ② 함수가 실제로 존재하는가
#        python3 로 들어가 dir(random) 을 찍어 목록을 직접 본다.
#   ③ 인자 이름이 맞는가
#        help(sorted) 로 인자 이름을 확인한다.
#
#   → 정답은 AI가 아니라 공식 문서에 있습니다. 셋을 다 확인해도 1분이 안 걸립니다.
#
# 실습 규칙 (반드시 지킬 것)
#   AI가 알려준 패키지는 pip install 하기 전에 PyPI 페이지를 먼저 엽니다.
#
# 그리고 가장 중요한 경고
#   여기서는 ModuleNotFoundError 가 나서 다행이었습니다.
#   슬롭스쿼팅(slopsquatting) 공격에서는 공격자가 그 이름을 미리 등록해 두기 때문에
#   pip install 이 "성공"하고 아무 오류도 나지 않습니다.
#   그래서 설치한 뒤가 아니라 설치하기 전에 확인해야 합니다.
# ---------------------------------------------------------------------------

import random
import statistics


def sample_scores(scores, k):
    return random.choices(scores, k=k)


def report(scores):
    avg = statistics.mean(scores)
    return f"평균 {avg}"


print(report([90, 80, 70]))
print(sample_scores([90, 80, 70, 60], 2))
sorted_scores = sorted([3, 1, 2], reverse=True)
print(sorted_scores)
