def calculate_total(cart):
    return sum(price * quantity for price, quantity in cart.values())