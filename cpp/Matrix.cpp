#include "Matrix.hpp"

template <size_t size_m, size_t size_n>
Matrix::Matrix(int m, int n, int (&vectors)[size_m][size_n]) : f_m(m), f_n(n) {
    f_rows = (Vector*) malloc(f_m * sizeof(Vector));
    for (int i=0; i<f_m; i++) {
        f_rows[i] = Vector(f_n, vectors[i]);
    }
}


int Matrix::index(int i, int j) {
    return f_rows[i].index(j);
}


void printMatrix(Matrix* A, bool print_dim) {
    
    int widths[A->f_m][A->f_n];
    for (int i=0; i<A->f_m; i++) {
        for (int j=0; j<A->f_n; j++) {
            widths[i][j] = num_digits(A->index(i, j));
        }
    }

    int maxes[A->f_m];
    for (int i=0; i<A->f_m; i++) {
        maxes[i] = max(widths[i], A->f_n);
    }
    int width = max(maxes, A->f_m) + 1;

    if (print_dim) printf("%d x %d:\n", A->f_m, A->f_n);
    else printf("\n");
    for (int i=0; i<A->f_m; i++) {
        printf("[");
        for (int j=0; j<A->f_n; j++) {
            printf("%*d", width, A->index(i, j));
        }
        printf(" ]\n");
    }
    
}