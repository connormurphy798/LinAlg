import Vector as V
import Utils

class Matrix:
    """
    A 2d array of numbers.
    
        m = number of rows
        n = number of columns
        rows = list of m vectors of size n
        aug = number of augmented columns (0 if matrix is not augmented)
    """

    def __init__(self, m, n, lst=None, aug=0):
        
        self.m = m
        self.n = n
        self.aug = aug

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
        if not isinstance(A, Matrix):
            raise TypeError("Can only add matrices to matrices")

        if self.m != A.m or self.n != A.n:
            raise ValueError("Can only add matrices of same dimensions")
        
        B = []
        for i in range(self.m):
            B.append(self.rows[i] + A.rows[i])
        return Matrix(self.m, self.n, B)
    

    def __sub__(self, A):
        if not isinstance(A, Matrix):
            raise TypeError("Can only subtract matrices from matrices")
        
        if self.m != A.m or self.n != A.n:
            raise ValueError("Can only subtract matrices of same dimensions.")
        
        B = []
        for i in range(self.m):
            B.append(self.rows[i] - A.rows[i])
        return Matrix(self.m, self.n, B)
    

    def __mul__(self, A):
        if isinstance(A, Matrix):
            m, p = self.m, A.n
            if self.n != A.m:
                raise ValueError("Width of left matrix must match height of right matrix")
            B = [[] for i in range(m)]
            At = trans(A)
            for i in range(m):
                for j in range(p):
                    B[i].append(self.rows[i].dot(At.rows[j]))
            return Matrix(m, p, B)
        elif isinstance(A, V.Vector):
            if self.n != A.n:
                raise ValueError("Size of vector must match width of matrix")
            return V.Vector(self.m, [row.dot(A) for row in A.rows])
        raise TypeError("Can only multiply a matrix by a matrix or a vector")       
        

    def __eq__(self, A):
        if isinstance(A, Matrix):
            if (self.m != A.m) or (self.n != A.n):
                return False
            for i in range(self.m):
                if self.rows[i] != A.rows[i]:
                    return False
            return True
        if isinstance(A, V.Vector):   # treats vectors as a matrix of width 1
            if (self.m != A.n) or (self.n != 1):
                return False
            for i in range(self.m):
                if self.rows[i].elems[0] != A.elems[i]:
                    return False
            return True
        return False


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
        aug_index = self.n - self.aug
        s = ""
        for i in range(self.m):
            s += "["
            for j in range(self.n):
                if j == aug_index:
                    s += " |"
                elem = self.rows[i].elems[j]
                if type(elem) == float:
                    s += f"{elem:>{c}.{2}f}"
                else:
                    s += f"{elem:>{c}}"
            s += " ]\n"
        return s


    def at(self, i, j):
        """
        returns the (i,j) entry of a matrix
        """
        if i >= self.m:
            raise ValueError("index out of range")
        return self.rows[i].at(j)


    def copy(self):
        """
        returns a deep copy of a matrix
        """
        return Matrix(self.m, self.n, lst=self.rows, aug=self.aug)


    def swap_rows_ip(self, a, b):
        """
        swaps rows a and b of a matrix
        """
        if (type(a) != int) or (type(b) != int):
            raise TypeError("Row numbers must be ints")
        temp = self.rows[a]
        self.rows[a] = self.rows[b]
        self.rows[b] = temp
    

    def swap_cols_ip(self, a, b):
        """
        swaps columns a and b of a matrix
        """
        if (type(a) != int) or (type(b) != int):
            raise TypeError("Row numbers must be ints")
        col_a = [row.elems[a] for row in self.rows]
        for i in range(self.m):
            self.rows[i].elems[a] = self.rows[i].elems[b]
            self.rows[i].elems[b] = col_a[i]


    def row_add(self, a, b, s=1):
        """
        adds s*(row a) to row b
        """
        if (type(a) != int) or (type(b) != int):
            raise TypeError("Row numbers must be ints")
        if (type(s) != int) and (type(s) != float):
            raise TypeError("Scaling factor must be a number")
        self.rows[b] += self.rows[a].times(s)


    def row_scale(self, a, s):
        """
        scales row a by s
        """
        if (type(a) != int):
            raise TypeError("Row number must be int")
        if (type(s) != int) and (type(s) != float):
            raise TypeError("Scaling factor must be a number")
        self.rows[a] = self.rows[a].times(s)


    def edit_entry(self, i, j, k):
        """
        matrix[i, j] = k
        """
        if (type(i) != int) or (type(j) != int):
            raise TypeError("Row and column numbers must be ints")
        self.rows[i].elems[j] = k


    def block(self, pos, size):
        """
        grabs a block of a matrix starting at entry (pos[0], pos[1])
        and of size size[0] by size[1]
        """
        x, y = pos[0], pos[1]
        dx, dy = size[0], size[1]

        if (x < 0 or x >= self.m or
            y < 0 or y >= self.n or
            x + dx > self.m or y + dy > self.n):
            raise ValueError("Cannot grab block that exceeds matrix bounds")
        
        lst = []
        for i in range(x, x+dx):
            lst.append(self.rows[i].elems[y:y+dy])
        
        return Matrix(dx, dy, lst)


    def det(self):
        """
        returns the determinant of a matrix
        """
        if self.m != self.n:
            raise ValueError("Determinant can only be calculated for square matrices")
        
        U, _, d = ref(self)
        det = 1
        for i in range(self.m):
            det *= U.at(i,i)
        
        det /= d
        return (round(det) if Utils.is_integer(det) else det)


    def get_non_augmented(self):
        """
        returns the first half of an augmented matrix
        """
        if self.aug == 0:
            raise ValueError("Matrix is not augmented")
        return self.block((0, 0), (self.m, self.n-self.aug))


    def get_augmented(self):
        """
        returns the second half of an augmented matrix
        """
        if self.aug == 0:
            raise ValueError("Matrix is not augmented")
        return self.block((0, self.n-self.aug), (self.m, self.aug))


def trans(A):
    """
    returns the transpose of A
    """
    if isinstance(A, Matrix):
        rows = [[] for _ in range(A.n)]
        for i in range(A.m):
            for j in range(A.n):
                rows[j].append(A.rows[i].elems[j])
        return Matrix(A.n, A.m, rows)
    if isinstance(A, V.Vector):
        return Matrix(1, A.n, [V.Vector(1, [elem]) for elem in A.elems])
    raise TypeError("Transpose can only be found for matrices and vectors")


def identity_matrix(n):
    """
    returns an identity matrix of size n
    """
    rows = []
    for i in range(n):
        rows.append([(1 if i==j else 0) for j in range(n)])
    return Matrix(n, n, rows)


def swap_rows(M, a, b):
    """
    returns a copy of matrix M with rows a and b swapped
    """
    Mstar = M.copy()
    Mstar.swap_rows_ip(a, b)
    return Mstar


def swap_cols(M, a, b):
    """
    returns a copy of matrix M with columns a and b swapped
    """
    Mstar = M.copy()
    Mstar.swap_cols_ip(a, b)
    return Mstar
    

def augment(A, b):
    """
    returns a new matrix which is A augmented with b.
    b can be either a vector of size m or a matrix of
    size m by x, for any x
    """
    if not isinstance(A, Matrix):
        raise TypeError("Can only augment matrices")
    lst = []
    if isinstance(b, Matrix):
        if A.m != b.m:
            raise ValueError("Can only augment using matrices with same number of rows")
        for i in range(A.m):
            lst.append(A.rows[i].elems + b.rows[i].elems)
        aug = b.n
    elif isinstance(b, V.Vector):
        if A.m != b.n:
            raise ValueError("Can only augment matrix of size m by n with vector of size m")
        for i in range(A.m):
            lst.append(A.rows[i].elems + [b.elems[i]])
        aug = 1
    else:
        raise TypeError("Can only augment using matrices or vectors")
        
    return Matrix(A.m, A.n + aug, lst, aug=aug)


def ref(A, elim_matrix=False):
    """
    returns a list containing:
        U = upper triangular matrix in row echelon form, result of gaussian elimination on A
    and, if elim_matrix:
        E = elimination matrix (product of elementary matrices, E*A = U)
    and:
        d = determinant scaling factor (used in calculating determinant from gaussian elimination)
    """
    U, m, n = A.copy(), A.m, A.n
    d = 1
    if elim_matrix:
        E = identity_matrix(m)
    else:
        E = None
    for j in range(min(m, n)):
        # ensure a non-zero pivot
        if U.rows[j].elems[j] == 0:
            found_new_pivot = False
            for i in range(j+1, m):
                if U.rows[i].elems[j] != 0:
                    U.swap_rows_ip(i, j)
                    d = -d
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

    return (U, E, d)


def rref(A, elim_matrix=False):
    """
    returns a list containing:
        U = upper triangular matrix in reduced row echelon form, result of gaussian elimination on A
    and, if elim_matrix:
        E = elimination matrix (product of elementary matrices, E*A = U)
    """
    U, E, _ = ref(A, elim_matrix)   # TODO: keep track of E
    m, n = A.m, A.n

    # loop over columns backwards: find pivot, scale to 1, then subtract from upper rows
    for j in range(min(m,n))[::-1]:
        pivot = U.at(j, j)
        if pivot:
            U.row_scale(j, 1/pivot)
            for i in range(0, j):
                U.row_add(j, i, -U.at(i, j))
    return U, E


def inverse(A):
    """
    returns a matrix A_inv, s.t. A*A_inv = A_inv*A = I_n.
    throws an error for non-square or singular matrices.
    """
    if A.m != A.n:
        raise ValueError("Non-square matrices are not invertible")
    n = A.n
    I = identity_matrix(n)
    augmented = augment(A, I)
    U = rref(augmented)[0]
    if U.get_non_augmented() != I:
        raise ValueError("Matrix is not invertible")
    return U.get_augmented()




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


    # A26 = augment(
    #     Matrix(3, 3, [[1, 2, 3], [5, 6, 7], [9, 10, 11]]),
    #     V.Vector(3, [4, 8, 12])
    # )
    # print(A26)

    # A27 = augment(
    #     Matrix(3, 3, [[1, 2, 3], [5, 6, 7], [9, 10, 11]]),
    #     Matrix(3, 4, [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]])
    # )
    # print(A27)

    # lst28 = [[i*6+j for j in range(6)] for i in range(6)]
    # A28 = Matrix(6, 6, lst28)
    # print(A28.block((1, 2), (3, 3)))

    # A29 = Matrix(3, 3, [[1, 4, 5], [2, 8, 10], [6, 2, 1]])  # no inverse
    # print(inverse(A29))

    A30 = Matrix(2, 2, [[-1, 1.5], [1, -1]])
    print(inverse(A30))

    A31 = Matrix(3, 3, [[1, 2, 3], [4, 5, 6], [7, 2, 9]])
    print(inverse(A31))

    # A32 = Matrix(2, 2, [[3, 7], [1, -4]])
    # print(A32.det())
    
