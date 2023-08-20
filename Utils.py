def is_integer(k, tol=10e-9):
    return abs(k - round(k)) <= tol
    

if __name__ == "__main__":
    print(is_int(4.0))
    print(is_int(4.1))
    print(is_int(4.00000000000001))
    print(is_int(3.9))
    print(is_int(3.99999999999999))
    print(is_int(0.00000000000001))
    print(is_int(-0.00000000000001))
