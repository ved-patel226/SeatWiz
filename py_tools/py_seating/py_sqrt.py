import math

def nearest_highest_square_root(n):
    root = math.isqrt(n)
            
    highest_square = (root + 1) ** 2
    return highest_square