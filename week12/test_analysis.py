import pandas as pd

from analysis import 정제, 반별평균


scores = pd.read_csv("scores_2026.csv")
mini = pd.read_csv("mini.csv")
정제된_scores = 정제(scores)
정제된_mini = 정제(mini)


def test_scores_clean_to_100_rows():
    assert len(정제된_scores) == 100


def test_only_two_classes_remain():
    assert set(정제된_scores["반"].unique()) == {"1반", "2반"}


def test_grouped_score_sum_matches_total():
    grouped_total = 정제된_scores.groupby("반")["점수"].sum().sum()
    assert grouped_total == 정제된_scores["점수"].sum()


def test_mini_first_class_average_is_80():
    assert 반별평균(정제된_mini)["1반"] == 80.0