import math

class Vector:
    """
    A 2d array of numbers.
    Supports addition, subtraction, dot products, and equality checks.
    """

    def __init__(self, size, lst=None):
        if lst:
            if size != len(lst):
                raise ValueError("Vector length does not match number of elements.")

        self.n = size
        if lst:
            self.elems = [x for x in lst]
        else:
            self.elems = [0] * size

    def __add__(self, v):
        if self.n != v.n:
            raise ValueError("Can only add vectors of same size.")
        
        u = []
        for i in range(self.n):
            u.append(self.elems[i] + v.elems[i])
        return Vector(self.n, u)
    
    def __sub__(self, v):
        if self.n != v.n:
            raise ValueError("Can only subtract vectors of same size.")
        
        u = []
        for i in range(self.n):
            u.append(self.elems[i] - v.elems[i])
        return Vector(self.n, u)
    
    def __str__(self):
        s = str(self.elems)
        return s
    
    def times(self, k):         
        if type(k) != int and type(k) != float:
            raise TypeError("Can only multiply vectors by scalars.")
        
        u = []
        for i in range(self.n):
            u.append(self.elems[i] * k)
        return Vector(self.n, u)

    def dot(self, v):
        if self.n != v.n:
            raise ValueError("Can only take dot product of vectors of same size.")
        
        d = 0
        for i in range(self.n):
            d += self.elems[i]*v.elems[i]
        return d
    
    def mag(self):
        w = 0
        for i in range(self.n):
            w += (self.elems[i])*(self.elems[i])
        w = math.sqrt(w)
        return w
    
    def copy(self):
        return Vector(self.n, self.elems)
            



if __name__ == "__main__":
    # checking operations
    v1 = Vector(4, [4, 5, 1, 2])
    v2 = Vector(4, [1, 3, 7, 7])
    v3 = v1 + v2
    v4 = v1 - v2
    print(f"v3 = {v3.elems}")
    print(f"v4 = {v4.elems}")

    v5 = Vector(8)
    print(f"v5 = {v5.elems}")
    print(v5)

    v6 = v1.times(3)
    print(f"v6 = {v6}")

    # errors
    # v6 = Vector(5, [3, 4, 2])
    # v7 = Vector(3, [1, 2, 3, 4, 5])
    # v8 = Vector(3, [1, 2, 3])
    #v9 = Vector(2, [1, 2])
    # v10 = v8 - v9

    # other functions
    # print(v1.dot(v2))
    # print(v1.dot(v5))
    # print(Vector(2, [1, 1]).mag())
    # print(Vector(4, [2, 2, 2, 2]).mag())

    v11 = Vector(2, [1, 2])
    v12 = Vector(2, [1, 2])
    v13 = v11
    v14 = v11.copy()
    print(id(v11) == id(v12))
    print(id(v11) == id(v13))
    print(id(v11) == id(v14))
    print(id(v11.elems) == id(v12.elems))
    print(id(v11.elems) == id(v13.elems))
    print(id(v11.elems) == id(v14.elems))
    
    
