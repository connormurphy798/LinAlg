def is_integer(k, tol=1e-9):
    return abs(k - round(k)) <= tol
    

if __name__ == "__main__":
    print(is_integer(4.0))
    print(is_integer(4.1))
    print(is_integer(4.00000000000001))
    print(is_integer(3.9))
    print(is_integer(3.99999999999999))
    print(is_integer(0.00000000000001))
    print(is_integer(-0.00000000000001))
