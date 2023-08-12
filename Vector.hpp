#pragma once

#include <stdio.h>
#include <stdlib.h>
#include <initializer_list>

#include "Utils.cpp"

struct Vector {
    Vector(int n, int* elems);

    Vector(int n, std::initializer_list<int> elems);

    bool operator==(Vector v);

    bool operator!=(Vector v);

    Vector operator+(Vector v);

    Vector operator-(Vector v);

    int operator*(Vector v);

    int f_n;
    int* f_elems;

};

void printVector(Vector v, bool even_spacing=false);