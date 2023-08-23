import Vector as V
import Matrix as M
import operator as O


def test_func(f, x, y):
    """
    test a function f given a list of inputs x and expected output y.
    returns a tuple containing:
        - whether f(x) == y (bool)
        - return value of f called on the inputs in x 
    """
    return f(*x) == y, f(*x)


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

        (O.sub, [vec[0], vec[1]], V.Vector(4, [3, 2, -6, -5])),
        (O.sub, [vec[2], vec[3]], vec[7]),
        (O.sub, [vec[4], vec[5]], V.Vector(1, [-2])),

        (O.eq, [vec[1], vec[6]], True),
        (O.eq, [vec[1], vec[0]], False),
        (O.eq, [vec[0], vec[2]], False),
        (O.eq, [vec[2]+vec[2], vec[7]], True),
        (O.eq, [vec[2]-vec[2], vec[8]], True),

        (O.ne, [vec[1], vec[6]], False),
        (O.ne, [vec[1], vec[0]], True),
        (O.ne, [vec[0], vec[2]], True),
        (O.ne, [vec[2]+vec[2], vec[7]], False),
        (O.ne, [vec[2]-vec[2], vec[8]], False),
    ]

    d = create_case_dict(cases, names)

    for i in range(len(cases)):
        print_test_group(d, i)
        passed, result = test_func(cases[i][0], cases[i][1], cases[i][2])
        if not v:
            print(f"\tTest {i}: {'Passed' if passed else f'Failed (expected {cases[i][2]}, got {result})'}")
        else:
            print(f"\tTest {i}: {'Passed' if passed else 'Failed'} (expected {cases[i][2]}, got {result})")

    

if __name__ == "__main__":
    test_vector_ops()