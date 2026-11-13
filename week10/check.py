# check.py  —  네 가지 상황을 모든 버전에 똑같이 먹여 봅니다 (10주차)
# ---------------------------------------------------------------------------
# 쓰는 법 (week10 폴더의 터미널에서, .py 없이)
#     python check.py v0_plain
#     python check.py v1_security
#     python check.py v2_analyst
#     python check.py v3_perf
#     python check.py v4_final
#     python check.py v5_review
#   python이 안 되면 py(윈도우) 또는 python3(맥)를 씁니다.
#
# 하는 일
#   1. 네 상황에서 load_scores가 돌려준 값(또는 예외)을 보여 줍니다.
#   2. 맨 아래 "비교표에 옮겨 적기"에 강의안 9쪽 정답과의 비교를 요약합니다.
#   3. 화면에 나온 내용을 logs/<모듈이름>.txt 에 그대로 저장합니다.
#
# 이 파일은 고치지 마세요. 받은 코드도 고치지 마세요.
# ---------------------------------------------------------------------------

import contextlib
import importlib
import io
import logging
import os
import platform
import re
import sys
import unicodedata
import warnings
from datetime import datetime

# ── 강의안 9쪽 기대 결과 ────────────────────────────────────────────────────
CASES = [
    # (파일, 설명, 요약표 이름, 정답)
    ("없는파일.csv", "파일이 없을 때", "없는 파일",
     {"error": "FileNotFoundError"}),
    ("scores.csv", "정상 파일 (지저분한 줄이 섞여 있음)", "scores.csv",
     {"rows": [("김하나", 88), ("최,네번", 77), ("김하나", 91),
               ("윤보람", 64), ("서한별", 95)],
      "skipped": [3, 4, 7, 8, 9]}),
    ("empty.csv", "헤더만 있고 내용이 없을 때", "empty.csv",
     {"rows": [], "skipped": []}),
    ("weird.csv", "점수가 1000점, 빈 칸, 공백, 중복 이름", "weird.csv",
     {"rows": [("박세찬", 88.5), ("한겨울", 77), ("윤보람", 88)],
      "skipped": [2, 3, 4, 5, 6, 9]}),
]
SKIP_REPORT_FILES = ["scores.csv", "weird.csv"]   # 건너뛴 줄 안내를 비교할 파일


# ── 화면 출력 + 기록 ────────────────────────────────────────────────────────
LOG_LINES = []


def out(text=""):
    print(text)
    LOG_LINES.append(text)


def width(s):
    """한글은 두 칸으로 셉니다 (표 줄 맞추기용)."""
    return sum(2 if unicodedata.east_asian_width(c) in "WF" else 1 for c in s)


def pad(s, w):
    return s + " " * max(0, w - width(s))


# ── 함수 실행: 반환값/예외 + 함수가 알린 내용(print, 경고, logging)을 모음 ──
class _Collect(logging.Handler):
    def __init__(self):
        super().__init__(logging.DEBUG)
        self.messages = []

    def emit(self, record):
        try:
            self.messages.append(f"[{record.levelname}] {record.getMessage()}")
        except Exception:
            pass


def run_case(load_scores, path):
    buf_out, buf_err = io.StringIO(), io.StringIO()
    handler = _Collect()
    root = logging.getLogger()
    old_level = root.level
    root.addHandler(handler)
    root.setLevel(logging.DEBUG)
    result, error = None, None
    try:
        with warnings.catch_warnings(record=True) as caught, \
                contextlib.redirect_stdout(buf_out), \
                contextlib.redirect_stderr(buf_err):
            warnings.simplefilter("always")
            try:
                result = load_scores(path)
            except Exception as e:          # 예외도 결과로 기록합니다
                error = e
    finally:
        root.removeHandler(handler)
        root.setLevel(old_level)

    notices = []
    for text in (buf_out.getvalue(), buf_err.getvalue()):
        notices += [ln for ln in text.splitlines() if ln.strip()]
    notices += [f"[경고] {w.message}" for w in caught]
    notices += handler.messages
    return result, error, notices


# ── 판정 도우미 ─────────────────────────────────────────────────────────────
def record_value(result, error):
    """비교표에 적을 값: 예외 이름, 또는 '종류 · 길이'."""
    if error is not None:
        return type(error).__name__
    try:
        return f"{type(result).__name__} · {len(result)}"
    except TypeError:
        return type(result).__name__


def same_score(a, b):
    # 88과 88.0은 같다고 봅니다. '88'(글자)이나 True는 점수가 아닙니다.
    if isinstance(a, bool) or not isinstance(a, (int, float)):
        return False
    return a == b


def matches(expect, result, error):
    if "error" in expect:
        return error is not None and type(error).__name__ == expect["error"]
    if error is not None or not isinstance(result, list):
        return False
    if len(result) != len(expect["rows"]):
        return False
    for got, (name, score) in zip(result, expect["rows"]):
        if not isinstance(got, tuple) or len(got) != 2:
            return False
        if got[0] != name or not same_score(got[1], score):
            return False
    return True


_ROW_PATTERNS = [
    # "3행", "3번째 줄", "3번 행", "3줄"  (단, "총 5행" 같은 개수는 제외)
    r"(?<!총)(?<!총 )(?<![\d.])(\d+)\s*(?:번째\s*(?:행|줄|라인)|번\s*(?:행|줄)|행|줄)",
    # "행 3", "행 번호: 3", "줄 3", "line 3", "row 3", "라인 3"
    r"(?:행|줄|라인|line|row)\s*(?:번호|number|no\.?)?\s*[:#=]?\s*(\d+)",
]


def find_rows(notices):
    """함수가 알린 내용에서 행 번호를 찾아냅니다 (자동이라 완벽하지 않습니다)."""
    rows = set()
    for text in notices:
        for pat in _ROW_PATTERNS:
            for m in re.finditer(pat, text, flags=re.IGNORECASE):
                rows.add(int(m.group(1)))
    return sorted(rows)


def short(text, limit=200):
    return text[:limit] + (" ..." if len(text) > limit else "")


# ── 본체 ────────────────────────────────────────────────────────────────────
def load_module(name):
    """모듈을 불러옵니다. 실패하면 이유를 출력하고 None을 돌려줍니다."""
    if not os.path.exists(f"{name}.py"):
        out(f"'{name}.py' 를 찾을 수 없습니다. week10 폴더에 있는지, 파일 이름이 맞는지 확인하세요.")
        return None
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            mod = importlib.import_module(name)
    except SyntaxError as e:
        out(f"'{name}.py' 를 읽다가 문법 오류가 났습니다: {e.msg} ({e.lineno}행)")
        out("  ```python 같은 마크다운 표시나 설명 문장이 파일에 들어갔는지 확인하세요.")
        out("  (마크다운 표시만 지울 수 있습니다. 코드 내용은 고치지 않습니다.)")
        return None
    except Exception as e:
        out(f"'{name}.py' 를 불러오다가 오류가 났습니다: {type(e).__name__}: {e}")
        out("  이 실패도 그대로 기록합니다. 코드를 고치지 마세요.")
        return None
    if not hasattr(mod, "load_scores"):
        out(f"'{name}.py' 안에 load_scores 함수가 없습니다.")
        return None
    return mod


def main():
    if len(sys.argv) < 2:
        print("쓰는 법:  python check.py <모듈이름>")
        print("예시   :  python check.py v1_security")
        return

    # 터미널 위치와 상관없이 check.py가 있는 폴더(week10)를 기준으로 실행
    here = os.path.dirname(os.path.abspath(__file__))
    os.chdir(here)
    sys.path.insert(0, here)

    name = os.path.basename(sys.argv[1]).replace(".py", "")
    if not os.path.exists(f"{name}.py"):
        print(f"'{name}.py' 를 찾을 수 없습니다. week10 폴더에 있는지, 파일 이름이 맞는지 확인하세요.")
        print("  (명령에는 .py 없이 v0_plain 처럼 씁니다)")
        return

    out("=" * 68)
    out(f"  {name}.py  검사")
    out("=" * 68)

    mod = load_module(name)
    summary = []                # (요약표 이름, 같음?, 기록할 값, 정답)
    found = {}                  # 파일 → 함수가 알린 행 번호

    if mod is not None:
        for path, why, label, expect in CASES:
            out(f"\n[{why}]  {path}")
            result, error, notices = run_case(mod.load_scores, path)

            if notices:
                out("  → 함수가 알린 내용:")
                for line in notices[:15]:
                    out(f"      {short(line, 120)}")
                if len(notices) > 15:
                    out(f"      ... (그 외 {len(notices) - 15}줄)")

            if error is not None:
                out(f"  → 예외: {type(error).__name__}: {error}")
            else:
                out(f"  → 돌려준 값의 종류: {type(result).__name__}")
                try:
                    out(f"  → 길이: {len(result)}")
                except TypeError:
                    pass
                out(f"  → 내용: {short(repr(result))}")

            if "error" in expect:
                answer = expect["error"]
            else:
                answer = f"list · {len(expect['rows'])}"
            ok = matches(expect, result, error)
            summary.append((label, ok, record_value(result, error), answer))
            found[path] = find_rows(notices)

    # ── 요약 ────────────────────────────────────────────────────────────
    out("\n" + "-" * 68)
    out("비교표에 옮겨 적기  (정답은 강의안 9쪽 기대 결과)")
    out("-" * 68)

    if mod is None:
        out("  함수를 실행하지 못했습니다. 모든 칸에 위 오류를 적습니다.")
        out("  정답과 같은 칸: 0 / 4")
        out("  건너뛴 줄 안내: X / X")
    else:
        out(f"  {pad('상황', 14)}{pad('내용까지 같음', 16)}{pad('기록할 값', 22)}정답")
        for label, ok, value, answer in summary:
            out(f"  {pad(label, 14)}{pad('O' if ok else 'X', 16)}{pad(value, 22)}{answer}")
        n_ok = sum(1 for _, ok, _, _ in summary if ok)
        out(f"\n  정답과 같은 칸: {n_ok} / 4")

        out("\n  건너뛴 줄 안내 (함수가 알린 행 번호, 자동으로 찾은 값이니 위 내용도 확인하세요)")
        marks = []
        for path in SKIP_REPORT_FILES:
            expect = next(c[3] for c in CASES if c[0] == path)
            got = found.get(path, [])
            same = got == expect["skipped"]
            marks.append("O" if same else "X")
            got_txt = ", ".join(map(str, got)) if got else "없음"
            ans_txt = ", ".join(map(str, expect["skipped"]))
            out(f"  {pad(path, 12)}안내한 행: {pad(got_txt, 20)}"
                f"정답: {pad(ans_txt, 18)}같음: {marks[-1]}")
        out(f"\n  → 비교표의 '건너뛴 줄 안내' 칸: {' / '.join(marks)}  (scores / weird)")
    out("-" * 68)

    # ── 실행 기록 저장 ─────────────────────────────────────────────────────
    os.makedirs("logs", exist_ok=True)
    log_path = os.path.join("logs", f"{name}.txt")
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    header = [f"실행 일시: {stamp}",
              f"파이썬: {platform.python_version()} ({platform.system()})",
              ""]
    with open(log_path, "w", encoding="utf-8") as f:
        f.write("\n".join(header + LOG_LINES) + "\n")
    print(f"\n실행 기록 저장: logs/{name}.txt")


if __name__ == "__main__":
    # 윈도우 터미널에서 출력할 수 없는 글자가 있어도 멈추지 않게 합니다
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(errors="replace")
        except Exception:
            pass
    main()
