import math

def euclidean_distance(index1, index2):
    x1, y1 = index1
    x2, y2 = index2
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def index_to_coordinates(index, width):
    row = index // width
    col = index % width
    return (row, col)