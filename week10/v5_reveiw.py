import csv
from decimal import Decimal, InvalidOperation


def load_scores(path):
    scores = []

    with open(path, newline="", encoding="utf-8-sig") as file:
        reader = csv.reader(file)
        header = next(reader, None)
        if header != ["name", "score"]:
            raise ValueError("CSV 헤더는 name,score여야 합니다.")

        previous_line_number = reader.line_num
        for row in reader:
            row_number = previous_line_number + 1
            previous_line_number = reader.line_num

            if not row:
                continue

            if len(row) != 2:
                print(f"{row_number}행 제외: 열 개수가 2개가 아닙니다.")
                continue

            name = row[0].strip()
            score_text = row[1].strip()

            if not name:
                print(f"{row_number}행 제외: 이름이 비어 있습니다.")
                continue
            if not score_text:
                print(f"{row_number}행 제외: 점수가 비어 있습니다.")
                continue

            try:
                decimal_score = Decimal(score_text)
            except InvalidOperation:
                print(f"{row_number}행 제외: 점수가 숫자가 아닙니다.")
                continue

            if (
                not decimal_score.is_finite()
                or not Decimal("0") <= decimal_score <= Decimal("100")
            ):
                print(f"{row_number}행 제외: 점수가 0~100 범위를 벗어났습니다.")
                continue

            if decimal_score == decimal_score.to_integral_value():
                score = int(decimal_score)
            else:
                score = float(decimal_score)
            scores.append((name, score))

    return scores