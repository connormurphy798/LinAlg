import Vector as V
import Utils

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
                elem = self.rows[i].elems[j]
                if type(elem) != float:
                    l = len(str(elem)) + 1
                else:
                    s = str(elem)
                    s = s[:s.index(".")+3]
                    l = len(s) + 1
                if l > c:
                    c = l
        
        # print each row vector
        s = ""
        for i in range(self.m):
            s += "["
            for j in range(self.n):
                elem = self.rows[i].elems[j]
                if type(elem) == float:
                    s += f"{elem:>{c}.{2}f}"
                else:
                    s += f"{elem:>{c}}"
            s += " ]\n"
        return s


    def at(self, i, j):
        if i >= self.m:
            raise ValueError("index out of range")
        return self.rows[i].at(j)


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


    def row_add(self, a, b, s=1):
        """
        add s*(row a) to row b
        """
        self.rows[b] += self.rows[a].times(s)


    def row_scale(self, a, s=1):
        self.rows[a] = self.rows[a].times(s)


    def edit_entry(self, i, j, k):
        """
        matrix[i, j] = k
        """
        self.rows[i].elems[j] = k


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
    

def ref(A, elim_matrix=False):
    """
    returns:
        U = upper triangular matrix in row echelon form, result of gaussian elimination on A
    and, if elim_matrix, returns a tuple containing U and:
        E = elimination matrix (product of elementary matrices, E*A = U)
    """
    U, m, n = A.copy(), A.m, A.n
    if elim_matrix:
        E = identity_matrix(m)
    for j in range(min(m, n)):
        # ensure a non-zero pivot
        if U.rows[j].elems[j] == 0:
            found_new_pivot = False
            for i in range(j+1, m):
                if U.rows[i].elems[j] != 0:
                    U.swap_rows_ip(i, j)
                    if elim_matrix:
                        elem_matrix = identity_matrix(m).swap_rows(i, j)
                        E = elem_matrix * E
                    found_new_pivot = True
                    break
            if not found_new_pivot:
                continue
        pivot = U.rows[j].elems[j]
        
        # make all non-pivot points below j = 0
        for i in range(j+1, m):
            elem = U.rows[i].elems[j]
            if elem != 0:
                s = -elem/pivot
                U.row_add(j, i, s)
                if elim_matrix:
                    elem_matrix = identity_matrix(m)
                    elem_matrix.edit_entry(i, j, s)
                    E = elem_matrix * E  

    if elim_matrix:
        return U, E
    return U


def rref(A, elim_matrix=False):
    """
    returns:
        U = upper triangular matrix in reduced row echelon form, result of gaussian elimination on A
    and, if elim_matrix, returns a tuple containing U and:
        E = elimination matrix (product of elementary matrices, E*A = U)
    """
    U, m, n = ref(A, elim_matrix), A.m, A.n
    if elim_matrix:
        U, E = U[0], U[1]
    # loop over columns backwards: find pivot, scale to 1, then subtract from upper rows
    for j in range(min(m,n))[::-1]:
        pivot = U.at(j, j)
        if pivot:
            U.row_scale(j, 1/pivot)
            for i in range(0, j):
                U.row_add(j, i, -U.at(i, j))
    return U

if __name__ == "__main__":
    """
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
    """

    # A20 = identity_matrix(2)
    # U20 = ref(A20, True)
    # print(U20[0])
    # print(U20[1])

    # A21 = Matrix(2, 2, [[1, 3], [2, 8]])
    # U21, E21 = ref(A21, True)
    # print(U21)
    # print(E21 * A21)

    # A22 = Matrix(2, 2, [[1, 3], [2, 6]])
    # U22, E22 = ref(A22, True)
    # print(U22)
    # print(E22 * A22)

    # A23 = Matrix(4, 4, [[2, 3, 3, 8], [10, 2, 4, 5], [1, 2, 0, 2], [4, 3, 7, 20]])
    # U23, E23 = ref(A23, True)
    # print(U23)
    # print(E23 * A23)

    # A24 = Matrix(3, 4, [[1, 3, 1, 9], [1, 1, -1, 1], [3, 11, 5, 35]])
    # U24, E24 = ref(A24, True)
    # print(U24)
    # print(E24 * A24)
    # U24 = rref(A24)
    # print(U24)

    # A25 = Matrix(3, 4, [[2, 1, -1, 8], [-3, -1, 2, -11], [-2, 1, 2, -3]])
    # U25 = rref(A25)
    # print(U25)


