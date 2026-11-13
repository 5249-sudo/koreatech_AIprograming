import csv
import math


def load_scores(path):
    scores = []
    with open(path, newline="", encoding="utf-8-sig") as file:
        reader = csv.reader(file)
        next(reader, None)
        for row in reader:
            line_number = reader.line_num
            if not row:
                continue
            if len(row) != 2 or not row[0].strip():
                print(f"{line_number}행 건너뜀: 잘못된 행")
                continue
            try:
                score = float(row[1])
            except ValueError:
                print(f"{line_number}행 건너뜀: 점수가 숫자가 아님")
                continue
            if not math.isfinite(score) or not 0 <= score <= 100:
                print(f"{line_number}행 건너뜀: 점수 범위 오류")
                continue
            if score.is_integer():
                score = int(score)
            scores.append((row[0], score))
    return scores