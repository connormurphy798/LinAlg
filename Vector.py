import math
import Utils

class Vector:
    """
    A 1d array of numbers.
    
        n = size of vector
        elems = list of n elements
    """

    def __init__(self, size, lst=None):
        if lst:
            if size != len(lst):
                raise ValueError("Vector length does not match number of elements.")

        self.n = size
        if lst:
            self.elems = [(round(x) if Utils.is_integer(x) else x) for x in lst]
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


    def __eq__(self, v):
        if self.n != v.n:
            return False
        for i in range(self.n):
            if self.elems[i] != v.elems[i]:
                return False
        return True
    

    def __ne__(self, v):
        return not (self==v)
    

    def __str__(self):
        s = str(self.elems)
        return s
    

    def times(self, k):
        """
        returns a vector times the scalar k
        """      
        if type(k) != int and type(k) != float:
            raise TypeError("Can only multiply vectors by scalars.")
        
        u = []
        for i in range(self.n):
            u.append(self.elems[i] * k)
        return Vector(self.n, u)


    def dot(self, v):
        """
        returns the inner product of two vectors
        """
        if self.n != v.n:
            raise ValueError("Can only take dot product of vectors of same size.")
        
        d = 0
        for i in range(self.n):
            d += self.elems[i]*v.elems[i]
        return d
    

    def mag(self):
        """
        returns the magnitude of a vector
        """
        w = 0
        for i in range(self.n):
            w += (self.elems[i])*(self.elems[i])
        w = math.sqrt(w)
        return w
    

    def at(self, i):
        """
        returns the ith entry of a vector
        """
        if i >= self.n:
            raise ValueError(f"index out of range")
        return self.elems[i]    


    def copy(self):
        """
        returns a deep copy of a vector
        """
        return Vector(self.n, self.elems)
            

def normalize(v):
    """
    returns a vector v scaled to a magnitude of 1
    """
    return v.times(1/v.mag())


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
    print(f"{v11} == {v12}: {v11==v12}")
    print(f"{v11} == {v1}: {v11==v1}")
    print(f"{v1} == {v2}: {v1==v2}")
    
    
