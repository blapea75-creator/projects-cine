# Earn 1 point for every ₱100 spent
def earn_points(total):
    return int(total // 100)

# Give a ₱50 discount for 100 points
def redeem_discount(points, total):
    if points >= 100:
        return total - 50, points - 100
    return total, points


a