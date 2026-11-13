def calculate_total(cart):
    total = 0

    for price, quantity in cart.values():
        item_total = price * quantity

        if quantity >= 3:
            item_total = round(item_total * 0.85)

        total += item_total

    return total