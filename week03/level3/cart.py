def calculate_total(cart):
    if not cart:
        return 0

    total = 0
    for price, count in cart.values():
        amount = price * count
        if count >= 3:
            amount = amount * 0.85
        total += amount

    return int(round(total))