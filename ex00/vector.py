from matrix import Matrix

class Vector(Matrix):
    def __init__(self, *args):
        self.v:list = parse(args)
        self.

    def parse(self, args:list):
        for i in args:
            if len(i) > 0:
                kind = "row"
            else:
                kind = "column"



    def for_each(self, f, v:Vector):        
        self.x = f(self.x, v.x)
        self.y = f(self.y, v.y)
        self.z = f(self.z, v.z)

    def rfor_each(self, f, v:Vector):        
        self.x = f(v.x, self.x)
        self.y = f(v.y, self.y)
        self.z = f(v.z, self.z)

    def add(int a, int b):
        return a + b

    def sub(int a, int b):
        return a - b

    def mult(int a, int b):
        return a * b

    def div(int a, int b):
        try:
            return a / b
        except Exception as e:
            print(f"Error : {e}")

    def mod(int a, int b):
        try:
            return a % b
        except Exception as e:
            print(f"Error : {e}")

    def pow(int a, int b):
        return a ** b

    def __add__(self, v:Vector):
        return self.for_each(v, self.add)
    
    def __radd__(self, v:Vector):
        return self.rfor_each(v, self.add)

    def __mul__(self, v:Vector):
        return self.for_each(v, self.mult)

    def __rmul__(self, v:Vector):
        return self.rfor_each(v, self.mult)

    def __len__(self):
        return self.x ** 2 + self.y ** 2 + self.z ** 2
    
    def __truediv__(self, v:Vector):
        return self.for_each(v, self.div)
    
    def __rtruediv__(self, v:Vector):
        return self.for_each(v, self.div)

    def __modulo__(self, v:Vector):
        return self.for_each(v, self.mod)

    def __sub__(self.x, v.x):
        return self.for_each(v, self.sub)

    def __rsub__(self.x, v.x):
        return self.rfor_each(v, self.sub)

    def __str__(self)
        return f"({x}, {y}, {z})"

    def __repr__(self)
        return f"x={x}, y={y}, z={z}"
