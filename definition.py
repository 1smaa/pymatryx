import math
import functools


def overload_value(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if len(args) == 1:
            return Element.value_return(*args, **kwargs)
        else:
            return Element.value_set(*args, **kwargs)
    return wrapper


def overload_index(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if len(args) == 1:
            return Element.index_return(*args, **kwargs)
        else:
            return Element.index_set(*args, **kwargs)
    return wrapper


class Element(object):
    def __init__(self, index: tuple, value: int) -> object:
        self.__index = index
        self.__value = value

    @overload_value
    def value(self):
        pass

    @overload_index
    def index(self):
        pass

    def value_return(self) -> int:
        return self.__value

    def index_return(self) -> tuple:
        return self.__index

    def value_set(self, n: int) -> None:
        self.__value = n

    def index_set(self, ind: tuple) -> None:
        self.__index = ind


class Matrix(Element):
    def __init__(self, matrix: list, k: int) -> object:
        if matrix:
            for x in matrix:
                for y in x:
                    matrix[x][y] = Element((x, y,), matrix[x][y])
        self.__matrix = matrix
        self.__k = k

    def __default(self, height: int, width: int) -> list:
        self.__matrix = [[Element((x, y,), 0)
                          for x in range(width)] for y in range(height)]

    def element(self, x: int, y: int) -> Element:
        return self.__matrix[x][y]

    def set(self, index: tuple, value: int) -> None:
        x, y = index
        self.__matrix[x][y] = Element(index, value)

    def definition(self, points: list, n: int) -> float:
        result = 0
        m = None
        for i in range(1, n, 1):
            x1, y1, x2, y2 = points[i][0], points[i][1], points[i -
                                                                1][0], points[i-1][1]
            partial = eval("((y1+y2)*(x1-x2))/2")
            if m is None or partial < m:
                m = partial
            result += partial
        min_index = self.__find_min(points)
        avg = result/n
        x, x_max, x_min, y_min, k = result, points[-1][0], points[0][0], points[min_index][1], self.__k
        return eval("((x-((x_max-x_min)*y_min))*(m/avg))/k")

    def locate(self, n: int, points: list, d: float) -> None:
        min_point, max_point = points[self.__find_min(
            points)], points[self.__find_max(points)]
        x_offset = math.ceil((points[n-1][0]-points[0][0])/d)
        y_offset = math.ceil((max_point[1]-min_point[1])/d)
        self.__default(y_offset, x_offset)
        for point in points:
            row = math.floor((point[1]-min_point[1])/d)
            column = math.floor((point[0]-points[0][0])/d)
            row -= 1 if row == y_offset else 0
            column -= 1 if column == x_offset else 0
            self.__matrix[row][column].value(1)
        self.__matrix.reverse()

    def __find_min(self, points: list) -> int:
        j = 0
        m = points[0][1]
        for i in range(1, len(points)):
            if points[i][1] < m:
                m = points[i][1]
                j = i
        return j

    def __find_max(self, points: list) -> int:
        j = 0
        m = points[0][1]
        for i in range(1, len(points)):
            if points[i][1] > m:
                m = points[i][1]
                j = i
        return j

    def __repr__(self) -> None:
        return "\n".join([" ".join(list(map(lambda x: str(x.value()), i))) for i in self.__matrix])

    def tune(self, points: list, n: int) -> None:
        for k in range(1, 25, 1):
            self.__k = k
            d = self.definition(points, n)
            self.locate(n, points, d)
            if self.__check():
                break
        print(self.__k)

    def __check(self) -> None:
        xs, ys = [], []
        for x, row in enumerate(self.__matrix):
            for y, element in enumerate(row):
                if element.value() == 1:
                    xs.append(x)
                    ys.append(y)
        if len(list(set(xs))) != len(xs) or len(list(set(ys))) != len(ys):
            return False
        else:
            return True
