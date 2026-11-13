def circle_area(radius):
    """
    입력: 정수(int) 또는 실수(float)인 반지름 radius
    처리: radius가 음수이면 0.0을 반환
         radius가 0 이상이면 math.pi * radius * radius로 원의 넓이를 구하고
         round(넓이, 2)로 소수 둘째 자리까지 반올림
    출력: 넓이(float)
    경계: 음수 반지름 → 0.0 반환
    """
    import math
    if radius < 0:
        return 0.0
    else:
        area = math.pi * radius * radius
        return round(area, 2)

for radius in [2, 0, -1, 1.5]:
    result = circle_area(radius)
    print(radius, repr(result), type(result).__name__)
