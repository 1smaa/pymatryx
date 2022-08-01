Points = list[tuple[float]]
Matrix = list[list[int]]


def check(p: tuple, h: int, w: int) -> bool:
    return p[0] < 0 or p[1] < 0 or p[0] >= w or p[1] >= h


def connect(matrix: Matrix, shape: tuple, p: tuple, endpoint: tuple) -> tuple:
    x, y = p
    height, width = shape
    c = [[-1, 0], [-1, 1], [0, 1], [1, 1], [1, 0]]
    min = None
    j = 0
    for i, add in enumerate(c):
        p = [x+add[0], y+add[1]]
        if check(p, height, width):
            continue
        d = ((endpoint[0]-p[0])**2)+((endpoint[1]-p[1])**2)
        if min is None or d <= min:
            min = d
            j = i
    x += c[j][0]
    y += c[j][1]
    matrix[x][y] = 1
    return matrix, x, y


def fill_out(points: Points, matrix: Matrix, shape: tuple) -> list:
    '''Given a matrix with some scattered points, this function connects them.'''
    c = points[0]
    for i in range(1, len(points), 1):
        e = points[i]
        while c != e:
            matrix, x, y = connect(matrix, shape, c, e)
            c = (x, y,)
    return matrix


def find_points(matrix: Matrix) -> Points:
    p = []
    for x, row in enumerate(matrix):
        for y, element in enumerate(row):
            if element == 1:
                p.append((x, y,))
    p.sort(key=lambda x: x[1])
    return p
