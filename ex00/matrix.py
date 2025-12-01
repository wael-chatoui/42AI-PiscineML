
class Matrix:
    def __init__(self, data: list[list[int]]) -> None:
        self.data = data

    @property
    def shape(self):
        return len(self.data), len(self.data[0]) if len(self.data) > 0 else 0

    def __add__(self, m):
        if isinstance(m, (int, float)):
            res = [[self.data[y][x] + m for x in range(len(self.data[y]))] for y in range(len(self.data))]
            return Matrix(res)
        if self.shape != m.shape:
            return
        res = [[self.data[y][x] + m.data[y][x] for x in range(len(self.data[y]))] for y in range(len(self.data))]
        return Matrix(res)

    def __radd__(self, m):
        return self.__add__(m)

    def __sub__(self, m):
        if isinstance(m, (int, float)):
            res = [[self.data[y][x] - m for x in range(len(self.data[y]))] for y in range(len(self.data))]
            return Matrix(res)
        if self.shape != m.shape:
            return
        res = [[self.data[y][x] - m.data[y][x] for x in range(len(self.data[y]))] for y in range(len(self.data))]
        return Matrix(res)

    def __rsub__(self, m):
        return m.__sub__(self)

    def __truediv__(self, m):
        if isinstance(m, (int, float)):
            if m == 0:
                raise ZeroDivisionError("Division by zero")
            res = [[self.data[y][x] / m for x in range(len(self.data[y]))] for y in range(len(self.data))]
            return Matrix(res)
        raise TypeError(f"Unsupported operation for type /: Matrix and {type(m)}")

    def __rtruediv__(self, m):
        return m.__truediv__(self)

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            res = [[self.data[y][x] * other for x in range(len(self.data[y]))] for y in range(len(self.data))]
            return Matrix(res)
        elif isinstance(other, Matrix):
            if other.shape[0] == self.shape[0] and other.shape[1] == 1:
                res = [[self.data[y][x] * other.data[y][0] for x in range(len(self.data[y]))] for y in range(len(self.data))]
                return Matrix(res)
        raise TypeError(f"Unsupported operation for type *: Matrix and {type(other)}")

    def __rmul__(self, m):
        return m.__mul__(self)

    def __str__(self) -> None:
        return str(self.data)

m: Matrix = Matrix([[1, 2, 3], [4,5,6], [7,8,9]])
m2: Matrix = Matrix([[5], [2], [1]])

print(type(m))
print(type(m2))
print(m * m2)
