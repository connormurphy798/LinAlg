#pragma once

#include "Utils.cpp"
#include "Vector.cpp"

struct Matrix {
public:
    template <size_t size_m, size_t size_n>
    Matrix(int m, int n, int (&vectors)[size_m][size_n]);

    //Matrix(int m, int n, std::initializer_list<int*> vectors);
    
    //Matrix(int m, int n, std::initializer_list<std::initializer_list<int>> vectors);

    bool operator==(Matrix A);

    bool operator!=(Matrix A);

    Matrix operator+(Matrix A);

    Matrix operator-(Matrix A);

    Matrix operator*(Matrix A);

    Vector operator*(Vector v);

    int index(int i, int j);

    int f_m;
    int f_n;
    Vector* f_rows;
    
};

void printMatrix(Matrix* A, bool print_dim=false);