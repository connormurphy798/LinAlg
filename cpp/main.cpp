/**
 *
 *	Connor Murphy, 2023
 * 
 **/

 #include <stdio.h>

 #include "Vector.cpp"
 #include "Matrix.cpp"
 #include "Utils.cpp"

 int main(int argc, char* argv[]) {
    
    printf("made array\n");
    int lst[4] = {1, 2, 3, 4};
    Vector v1 = Vector(4, lst);
    printVector(v1);
    printf("\n");

    Vector v2 = Vector(4, {9, 10, 11, 12});
    printVector(v2);
    printf("\n");

    Vector v3 = Vector(6, {46, 1, 22222, 42, 105, 8});
    printVector(v3);
    printf("\n");

    Vector v4 = Vector(6, {77777, 46, 1, 42, 105, 8});
    Vector v5 = Vector(6, {46, 1, 105, 2, 33333, 8});
    Vector v6 = Vector(6, {77777, 46, 1, 42, 105, 99999});
    printVector(v3, true);
    printf("\n");
    printVector(v4, true);
    printf("\n");
    printVector(v5, true);
    printf("\n");
    printVector(v6, true);
    printf("\n");

    // -------------------------------------------------------------

    int nums[4][3] = {{7, 11, 400}, {2, 5, 4}, {8, 12, 6}, {10, 9, 1}};
    Matrix A1 = Matrix(4, 3, nums);
    printMatrix(&A1, true);

    return 0;
 }