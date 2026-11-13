# 섭씨 온도를 화씨로 바꾸는 함수 celsius_to_fahrenheit를 만든다
# 매개변수: celsius (숫자)
# 반환값: 화씨 온도 (숫자)
def celsius_to_fahrenheit(celsius):
    fahrenheit = (celsius * 9/5) + 32
    return fahrenheit

print(celsius_to_fahrenheit(0))
print(celsius_to_fahrenheit(100))
print(celsius_to_fahrenheit(-40))
