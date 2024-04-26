# A function to calculate the square root
def square_root(n):
    if n == 0:
        return 0

    x = n
    while True:
        root = (x + n / x) / 2
        if abs(root - x) < 0.0001:  # tolerance
            break
        x = root

    return root
