def clean_strings(items: list[str]) -> list[str]:
    result = []
    seen = set()

    for item in items:
        if item.strip() == "":
            continue

        key = item.casefold()

        if key not in seen:
            result.append(item)
            seen.add(key)

    return result


print(clean_strings(["A", "a", "A"]))
# ["A"]

print(clean_strings(["Hello", "World", "hello", "   ", "Python"]))
# ["Hello", "World", "Python"]