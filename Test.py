import Vector as V
import Matrix as M
import operator as O

import math


def test_func(f, x, y, tol=1e-6):
    """
    test a function f given a list of inputs x and expected output y.
    returns a tuple containing:
        - whether f(x) == y (bool), to within tol if f(x) is a float
        - return value of f called on the inputs in x 
    """
    try:
        f_x = f(*x)
    except Exception as e:
        f_x = type(e)
    eq = (f_x == y) if (type(f_x) != float) else (abs(f_x - y) < tol)
    return eq, f_x


def test_method(m, o, x, y, tol=1e-6):
    """
    tests the return value of a method m given an object o,
    a list of inputs x, and expected output y.
    returns a tuple containing:
        - whether o.m(x) == y (bool), to within tol if o.m(x) is a float
        - return value of m called on o and the inputs in x
    NB: does not test whether m correctly handles side effects
    """
    try:
        om_x = getattr(o, m.__name__)(*x)
    except Exception as e:
        om_x = type(e)
    eq = (om_x == y) if (type(om_x) != float) else (abs(om_x - y) < tol)
    return eq, om_x


def create_case_dict(cases: list, names: dict):
    """
    cases = list of test cases
    names = dictionary mapping functions to descriptive strings
    returns a dictionary mapping the first index in cases at which a function
    occurs to its descriptive name
    """
    case_d = {}
    funcs = set()
    for i in range(len(cases)):
        f = cases[i][0]
        if f not in funcs:
            funcs.add(f)
            case_d[i] = names[f]
    return case_d


def print_test_group(d: dict, i: int):
    """
    prints d[i] if i is in d, otherwise does nothing
    """
    if i in d:
        print(d[i])


def run_func_tests(cases: list, names: dict, v: bool):
    d = create_case_dict(cases, names)
    for i in range(len(cases)):
        print_test_group(d, i)
        passed, result = test_func(cases[i][0], cases[i][1], cases[i][2])
        if not v:
            print(f"\tTest {i}: {'Passed' if passed else f'Failed (expected {cases[i][2]}, got {result})'}")
        else:
            print(f"\tTest {i}: {'Passed' if passed else 'Failed'} (expected {cases[i][2]}, got {result})")
    print()


def run_method_tests(cases: list, names: dict, v: bool):
    d = create_case_dict(cases, names)
    for i in range(len(cases)):
        print_test_group(d, i)
        passed, result = test_method(cases[i][0], cases[i][1], cases[i][2], cases[i][3])
        if not v:
            print(f"\tTest {i}: {'Passed' if passed else f'Failed (expected {cases[i][3]}, got {result})'}")
        else:
            print(f"\tTest {i}: {'Passed' if passed else 'Failed'} (expected {cases[i][3]}, got {result})")
    print()


def test_vector_ops(v=False):
    """
    Tests supported vector operators: +, -, ==, and !=.
    """

    print(f"Testing vector operators:{' (verbose feedback)' if v else ''}")
    
    vec = [
        V.Vector(4, [4, 5, 1, 2]),  # 0
        V.Vector(4, [1, 3, 7, 7]),
        V.Vector(3, [17, 0, 1]),
        V.Vector(3, [-17, 0, -1]),

        V.Vector(1, [6]),           # 4
        V.Vector(1, [8]),
        V.Vector(4, [1, 3, 7, 7]),
        V.Vector(3, [34, 0, 2]),

        V.Vector(3),                # 8
        V.Vector(4)
    ]

    names = {
        O.add : "\n\tAddition (+):",
        O.sub : "\n\tSubtraction (-):",
        O.eq  : "\n\tEquality (==):",
        O.ne  : "\n\tInequality (!=):"
    }

    cases = [   # (op, [inputs], expected)
        (O.add, [vec[0], vec[1]], V.Vector(4, [5, 8, 8, 9])),
        (O.add, [vec[2], vec[3]], V.Vector(3, [0, 0, 0])),
        (O.add, [vec[2], vec[3]], vec[8]),
        (O.add, [vec[4], vec[5]], V.Vector(1, [14])),
        (O.add, [vec[2], vec[2]], V.Vector(3, [34, 0, 2])),
        (O.add, [vec[1], vec[2]], ValueError),
        (O.add, [vec[4], vec[8]], ValueError),

        (O.sub, [vec[0], vec[1]], V.Vector(4, [3, 2, -6, -5])),
        (O.sub, [vec[2], vec[3]], vec[7]),
        (O.sub, [vec[4], vec[5]], V.Vector(1, [-2])),
        (O.sub, [vec[0], vec[2]], ValueError),
        (O.sub, [vec[9], vec[8]], ValueError),

        (O.eq, [vec[1], vec[6]], True),
        (O.eq, [vec[1], vec[0]], False),
        (O.eq, [vec[0], vec[2]], False),
        (O.eq, [vec[2]+vec[2], vec[7]], True),
        (O.eq, [vec[2]-vec[2], vec[8]], True),

        (O.ne, [vec[1], vec[6]], False),
        (O.ne, [vec[1], vec[0]], True),
        (O.ne, [vec[0], vec[2]], True),
        (O.ne, [vec[2]+vec[2], vec[7]], False),
        (O.ne, [vec[2]-vec[2], vec[8]], False)
    ]

    run_func_tests(cases, names, v)


def test_vector_methods(v=False):
    """
    Tests vector methods: .times(), .dot(), .mag(), and .at().
    """
    print(f"Testing vector methods:{' (verbose feedback)' if v else ''}")
    
    vec = [
        V.Vector(4, [4, 5, 1, 2]),  # 0
        V.Vector(4, [1, 3, 7, 7]),
        V.Vector(3, [17, 0, 1]),
        V.Vector(3, [-17, 0, -1]),

        V.Vector(1, [6]),           # 4
        V.Vector(1, [8]),
        V.Vector(4, [1, 3, 7, 7]),
        V.Vector(3, [34, 0, 2]),

        V.Vector(3),                # 8
        V.Vector(4)
    ]

    names = {
        V.Vector.times : "\n\tScalar multiplication (times):",
        V.Vector.dot   : "\n\tInner product (dot):",
        V.Vector.mag   : "\n\tMagnitude (mag):",
        V.Vector.at    : "\n\tGet nth element (at):",
    }


    cases = [   # (method, object, [inputs], expected)
        (V.Vector.times, vec[0], [3], V.Vector(4, [12, 15, 3, 6])),
        (V.Vector.times, vec[0], [2.0], V.Vector(4, [8.0, 10.0, 2.0, 4.0])),
        (V.Vector.times, vec[2], [1], vec[2]),
        (V.Vector.times, vec[2], [0], vec[8]),
        (V.Vector.times, vec[2], [vec[1]], TypeError),

        (V.Vector.dot, vec[4], [vec[5]], 48),
        (V.Vector.dot, vec[5], [vec[4]], 48),
        (V.Vector.dot, vec[2], [vec[3]], -290),
        (V.Vector.dot, vec[3], [vec[2]], -290),
        (V.Vector.dot, vec[7], [vec[8]], 0),
        (V.Vector.dot, vec[0], [vec[4]], ValueError),
        
        (V.Vector.mag, vec[0], [], math.sqrt(46)),
        (V.Vector.mag, vec[1], [], 10.392304845),
        (V.Vector.mag, vec[2], [], math.sqrt(290)),
        (V.Vector.mag, vec[3], [], math.sqrt(290)),
        (V.Vector.mag, vec[4], [], 6.0),
        (V.Vector.mag, vec[5], [], math.sqrt(64.0)),
        (V.Vector.mag, vec[8], [], 0.0),

        (V.Vector.at, vec[0], [0], 4),
        (V.Vector.at, vec[0], [1], 5),
        (V.Vector.at, vec[0], [-2], 1),
        (V.Vector.at, vec[0], [-1], 2),
        (V.Vector.at, vec[2], [3], IndexError)
    ]

    run_method_tests(cases, names, v)


def test_matrix_ops(v=False):
    """
    Tests supported matrix operators: +, -, *, ==, and !=.
    """
    print(f"Testing matrix operators:{' (verbose feedback)' if v else ''}")
    
    mat = [
        M.Matrix(3, 3, [[1, 2, 3], [4, 5, 6], [7, 8, 9]]),  # 0
        M.Matrix(3, 3, [[4, 5, 6], [7, 8, 9], [1, 2, 3]]),
        M.Matrix(2, 3, [[7, 2, 1], [5, 5, 3]]),
        M.Matrix(2, 3, [[2, 6, 4], [4, 2, 9]]),

        M.Matrix(3, 4, [[7, 2, 4, 6], [6, 3, 0, 1], [2, 5, 2, 6]]),           # 4
        M.Matrix(3, 3),
        M.Matrix(2, 2),
        M.Matrix(2, 2, [[3, 1], [4, 1]]),

        M.Matrix(3, 3, [[0, 0, 0], [0, 0, 0], [0, 0, 0]]),  # 8
        M.Matrix(2, 3, [[2, 6, 4], [4, 2, 9]])

    ]

    names = {
        O.add : "\n\tAddition (+):",
        O.sub : "\n\tSubtraction (-):",
        O.mul : "\n\tMultiplication (*)",
        O.eq  : "\n\tEquality (==):",
        O.ne  : "\n\tInequality (!=):"
    }


    cases = [   # (op, [inputs], expected)
        (O.add, [mat[0], mat[1]], M.Matrix(3, 3, [[5, 7, 9], [11, 13, 15], [8, 10, 12]])),
        (O.add, [mat[0], mat[0]], M.Matrix(3, 3, [[2, 4, 6], [8, 10, 12], [14, 16, 18]])),
        (O.add, [mat[2], mat[3]], M.Matrix(2, 3, [[9, 8, 5], [9, 7, 12]])),
        (O.add, [mat[1], mat[5]], mat[1]),
        (O.add, [mat[0], mat[4]], ValueError),
        (O.add, [mat[0], mat[6]], ValueError),


        (O.sub, [mat[1], mat[0]], M.Matrix(3, 3, [[3, 3, 3], [3, 3, 3], [-6, -6, -6]])),
        (O.sub, [mat[0], mat[0]], M.Matrix(3, 3)),
        (O.sub, [mat[2], mat[3]], M.Matrix(2, 3, [[5, -4, -3], [1, 3, -6]])),
        (O.sub, [mat[7], mat[6]], mat[7]),
        (O.sub, [mat[5], mat[4]], ValueError),
        (O.sub, [mat[0], mat[6]], ValueError),

        (O.mul, [mat[0], mat[1]], M.Matrix(3, 3, [[21, 27, 33], [57, 72, 87], [93, 117, 141]])),
        (O.mul, [mat[0], mat[5]], mat[8]),
        (O.mul, [mat[1], mat[4]], M.Matrix(3, 4, [[70, 53, 28, 65], [115, 83, 46, 104], [25, 23, 10, 26]])),
        (O.mul, [mat[4], mat[1]], ValueError),
        (O.mul, [mat[7], M.identity_matrix(2)], mat[7]),
        (O.mul, [mat[2], V.Vector(3, [3, 2, 1])], V.Vector(2, [26, 28])),
        (O.mul, [mat[2], V.Vector(2, [2, 1])], ValueError),

        (O.eq, [mat[5], mat[8]], True),
        (O.eq, [mat[3], mat[9]], True),
        (O.eq, [mat[0]-mat[0], mat[5]], True),
        (O.eq, [mat[0], mat[1]], False),
        (O.eq, [mat[0], mat[2]], False),
        (O.eq, [mat[0], mat[4]], False),
        (O.eq, [mat[3], mat[3]], True),

        (O.ne, [mat[5], mat[8]], False),
        (O.ne, [mat[3], mat[9]], False),
        (O.ne, [mat[0]-mat[0], mat[5]], False),
        (O.ne, [mat[0], mat[1]], True),
        (O.ne, [mat[0], mat[2]], True),
        (O.ne, [mat[0], mat[4]], True),
        (O.ne, [mat[3], mat[3]], False)
    ]

    run_func_tests(cases, names, v)


if __name__ == "__main__":
    # test_vector_ops()
    # test_vector_methods()
    test_matrix_ops()