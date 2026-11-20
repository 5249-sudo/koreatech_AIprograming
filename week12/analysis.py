import pandas as pd

def 정제(df):
    정제_df = df.copy()
    print(len(정제_df))

    # 점수가 비어 있는 행을 삭제한다.
    정제_df = 정제_df.dropna(subset=["점수"])
    print(len(정제_df))

    # 모든 열이 완전히 같은 중복 행을 하나만 남긴다.
    정제_df = 정제_df.drop_duplicates()
    print(len(정제_df))

    # 반과 과목의 앞뒤 공백을 제거한다.
    정제_df["반"] = 정제_df["반"].str.strip()
    정제_df["과목"] = 정제_df["과목"].str.strip()

    # 점수가 0~100 범위를 벗어난 행을 삭제한다.
    정제_df = 정제_df[정제_df["점수"].between(0, 100)]
    print(len(정제_df))

    return 정제_df

df = 정제(pd.read_csv("scores_2026.csv"))

print(sorted(df["반"].unique())) 

print(sorted(df["과목"].unique()))

수학_df = df[df["과목"] == "수학"]
print(len(수학_df))

반1_90점이상_df = df[(df["반"] == "1반") & (df["점수"] >= 90)]
print(len(반1_90점이상_df))

반별_점수_평균 = df.groupby("반")["점수"].mean()
print(반별_점수_평균)

과목_반별_점수_평균 = df.groupby(["과목", "반"])["점수"].mean()
print(과목_반별_점수_평균)


def 반별평균(df):
    통계표 = df.groupby("반")["점수"].agg(["count", "mean", "median", "max"]).round(2)
    통계표.columns = ["개수", "평균", "중앙값", "최댓값"]
    print(통계표)
    return 통계표["평균"]


반별평균(df)

print(반별평균(df)["1반"])

# ② — 합계일치그룹으로나눠도총합은변하지않아야합니다
print(df.groupby("반")["점수"].sum().sum())   # 7484.0
print(df["점수"].sum())                        # 7484.0   ←같아야합니다
print(df.groupby("반")["점수"].count().sum())  # 100
print(len(df))                                 # 100      ←같아야합니다
# ④ — 스팟체크결과표에서한칸을골라원본에서직접셉니다
print(df[(df["반"] == "1반") & (df["과목"] == "수학")]["점수"])
#  →여덟개의값이나옵니다. 계산기로더해서8로나눠보세요.
#  →과목× 반평균표의1반· 수학60.0 과같습니까?

미니 = 정제(pd.read_csv("mini.csv"))
print( 반별평균(미니))