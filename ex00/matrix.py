
class ShapeError(Exception):
    """Exception raised when matrix shapes don't match for an operation."""
    pass

class MatrixTypeError(TypeError):
    """Exception raised when input is not a valid matrix."""
    pass

class Matrix:
    def __init__(self, data: list[list[int]]) -> None:
        if not isinstance(data, list):
            raise MatrixTypeError(f"Expected list, got {type(data).__name__}")
        if not all(isinstance(row, list) for row in data):
            raise MatrixTypeError("All elements must be lists (matrix rows)")
        if len(data) > 0:
            row_length = len(data[0])
            if not all(len(row) == row_length for row in data):
                raise ShapeError("All rows must have the same length")
        self.data = data

    @property
    def shape(self):
        return len(self.data), len(self.data[0]) if len(self.data) > 0 else 0

    def is_scalar(sef, v):
        return isinstance(v, (int, float))
    
    def scalar_to_matrix(self, nb):
        if isinstance(nb, (int, float)):
            if self.shape:
                return Matrix([[nb] for i in range(self.shape[0])])
            else:
                print("Warning : Matrix has no shape. Couldn't generate scalar from no shape")
        else:
            raise ValueError("nb is not a number")

    def __add__(self, m):
        if self.is_scalar(m):
            m = self.scalar_to_matrix(m)
        if not isinstance(m, Matrix):
            raise MatrixTypeError(f"Cannot add Matrix with {type(m).__name__}")
        if self.shape != m.shape:
            raise ShapeError(f"Cannot add matrices with different shapes: {self.shape} and {m.shape}")
        res = [[self.data[y][x] + m.data[y][x] for x in range(len(self.data[y]))] for y in range(len(self.data))]
        return Matrix(res)

    def __sub__(self, m):
        if self.is_scalar(m):
            m = self.scalar_to_matrix(m)
        if not isinstance(m, Matrix):
            raise MatrixTypeError(f"Cannot subtract {type(m).__name__} from Matrix")
        if self.shape != m.shape:
            raise ShapeError(f"Cannot subtract matrices with different shapes: {self.shape} and {m.shape}")
        res = [[self.data[y][x] - m.data[y][x] for x in range(len(self.data[y]))] for y in range(len(self.data))]
        return Matrix(res)

    def __truediv__(self, m):
        if isinstance(m, (int, float)):
            if m == 0:
                raise ZeroDivisionError("Division by zero")
            res = [[self.data[y][x] / m for x in range(len(self.data[y]))] for y in range(len(self.data))]
            return Matrix(res)
        raise TypeError(f"Unsupported operation for type /: Matrix and {type(m)}")

    def __mul__(self, other):
        if self.is_scalar(other):
            other = self.scalar_to_matrix(other)
        if not isinstance(other, Matrix):
            raise MatrixTypeError(f"Cannot multiply Matrix with {type(other).__name__}")
        if other.shape[0] != self.shape[0] or other.shape[1] != 1:
            raise ShapeError(f"Incompatible shapes for multiplication: {self.shape} and {other.shape}")
        res = [[self.data[y][x] * other.data[y][0] for x in range(len(self.data[y]))] for y in range(len(self.data))]
        return Matrix(res)

    def __radd__(self, m):
        return self.__add__(m)

    def __rsub__(self, m):
        return m.__sub__(self)

    def __rtruediv__(self, m):
        return m.__truediv__(self)
    
    def __rmul__(self, m):
        return m.__mul__(self)

    def __str__(self) -> None:
        return str(self.data)

m: Matrix = Matrix([[1, 2, 3], [4,5,6], [7,8,9]])
m2: Matrix = Matrix([[5], [2], [1]])

print(m * m2)
print(m * 2)
print(m.scalar_to_matrix(6))