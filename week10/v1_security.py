import csv


def load_scores(path):
    with open(path, newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        scores = []
        for row in reader:
            score = float(row["score"])
            if score.is_integer():
                score = int(score)
            scores.append((row["name"], score))
        return scores