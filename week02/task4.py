def celsius_to_fahrenheit(celsius):
    fahrenheit = (celsius * 9/5) + 32
    return fahrenheit

from task4 import celsius_to_fahrenheit

print(celsius_to_fahrenheit(0))
print(celsius_to_fahrenheit(100))
print(celsius_to_fahrenheit(-40))
print(celsius_to_fahrenheit(37))
print(round(celsius_to_fahrenheit(-273.15), 2))