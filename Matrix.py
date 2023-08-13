import Vector as V

class Matrix:
    """
    A 2d array of numbers.
    
        m = number of rows
        n = number of columns
        rows = list of m vectors of size n
    """

    def __init__(self, m, n, lst=None):
        
        self.m = m
        self.n = n

        if lst:
            if m != len(lst):
                raise ValueError(f"Number of row vectors does not match matrix dimension (expected {m}, got {len(lst)})")


        self.rows = []
        if lst:
            for i in range(m):
                if isinstance(lst[i], V.Vector):
                    if lst[i].n != n:
                        raise ValueError(f"Length of matrix rows does not match provided dimension (expected {n}, got {len(lst[i])})")
                    self.rows.append(lst[i].copy())
                else:
                    if len(lst[i]) != n:
                        raise ValueError(f"Length of matrix rows does not match provided dimension (expected {n}, got {len(lst[i])})")
                    self.rows.append(V.Vector(n, lst[i]))
        else:
            for i in range(m):
                self.rows.append(V.Vector(n))


    def __add__(self, A):
        if self.m != A.m or self.n != A.n:
            raise ValueError("Can only add matrices of same dimensions.")
        
        B = []
        for i in range(self.m):
            B.append(self.rows[i] + A.rows[i])
        return Matrix(self.m, self.n, B)
    

    def __sub__(self, A):
        if self.m != A.m or self.n != A.n:
            raise ValueError("Can only subtract matrices of same dimensions.")
        
        B = []
        for i in range(self.m):
            B.append(self.rows[i] - A.rows[i])
        return Matrix(self.m, self.n, B)
    

    def __mul__(self, A):
        m, n, p = self.m, self.n, A.n
        if self.n != A.m:
            raise ValueError("Width of left matrix must match height of right matrix.")
        B = [[] for i in range(m)]
        At = trans(A)
        for i in range(m):
            for j in range(p):
                B[i].append(self.rows[i].dot(At.rows[j]))
        return Matrix(m, p, B)
        

    def __eq__(self, A):
        if (self.m != A.m) or (self.n != A.n):
            return False
        for i in range(self.m):
            if self.rows[i] != A.rows[i]:
                return False
        return True


    def __ne__(self, A):
        return not (self == A)


    def __str__(self):
        # find max number of digits in any number
        c = 2
        for i in range(self.m):
            for j in range(self.n):
                l = len(str(self.rows[i].elems[j])) + 1
                if l > c:
                    c = l
        
        # print each row vector
        s = ""
        for i in range(self.m):
            s += "["
            for j in range(self.n):
                s += f"{self.rows[i].elems[j]:>{c}}"
            s += " ]\n"
        return s


    def copy(self):
        lst = []
        for row in self.rows:
            lst.append(row.copy())
        return Matrix(self.m, self.n, lst)


    def swap_rows_ip(self, a, b):
        temp = self.rows[a]
        self.rows[a] = self.rows[b]
        self.rows[b] = temp
    

    def swap_cols_ip(self, a, b):
        col_a = [row.elems[a] for row in self.rows]
        for i in range(self.m):
            self.rows[i].elems[a] = self.rows[i].elems[b]
            self.rows[i].elems[b] = col_a[i]


def trans(A):
    rows = [[] for i in range(A.n)]
    for i in range(A.m):
        for j in range(A.n):
            rows[j].append(A.rows[i].elems[j])
    return Matrix(A.n, A.m, rows)


def identity_matrix(n):
    rows = []
    for i in range(n):
        rows.append([(1 if i==j else 0) for j in range(n)])
    return Matrix(n, n, rows)


def swap_rows(M, a, b):
    Mstar = M.copy()
    Mstar.swap_rows_ip(a, b)
    return Mstar


def swap_cols(M, a, b):
    Mstar = M.copy()
    Mstar.swap_cols_ip(a, b)
    return Mstar
    

def gaussian_elimination(A, elim_matrix=False):
    """
    returns a pair of matrices:
        U = upper triangular matrix, result of gaussian elimination on A
        E = elimination matrix (product of elementary matrices, E*A = U)
    """
    return None


if __name__ == "__main__":
    A1 = Matrix(3, 3, [[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    A2 = Matrix(3, 3, [[4, 5, 6], [7, 8, 9], [1, 2, 3]])
    print(A1)
    print(A2)
    A3 = A1 + A2
    A4 = A1 - A2
    print(A3)
    print(A4)

    A5 = Matrix(4, 3, [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]])
    print(trans(A5))



    # A_t = trans(A)
    # A.trans()
    A6 = Matrix(2, 2, [[0, 2], [3, 0]])
    A7 = Matrix(2, 2, [[3, 1], [4, 7]])
    print(A6*A7)
    # print(A1*A6)

    A8 = Matrix(3, 2, [[1, 5], [6, 2], [7, 7]])
    A9 = Matrix(2, 4, [[1, 2, 3, 4], [5, 6, 7, 8]])
    print(A8*A9)

    A10 = swap_rows(A8, 1, 2)
    print(A8)
    print(A10)
    A8.swap_rows_ip(1, 2)
    print(A8)
    print(A10)

    print(A9)
    A11 = swap_cols(A9, 1, 2)
    print(A9)
    print(A11)
    A9.swap_cols_ip(1, 2)
    print(A9)
    print(A11)

    print(identity_matrix(5))
    print(f"These two:\n{A8}{A9}{A8==A9}")
    print(f"These two:\n{A8}{A10}{A8==A10}")
    print(f"These two:\n{A6}{A7}{A6==A7}")




