#pragma once

#include "Vector.hpp"

Vector::Vector(int n, int* elems) : f_n(n) {
    f_elems = (int*) malloc(f_n * sizeof(int));
    for (int i=0; i<f_n; i++) {
        f_elems[i] = elems[i];
    }
}

Vector::Vector(int n, std::initializer_list<int> elems) : f_n(n) {
    f_elems = (int*) malloc(f_n * sizeof(int));
    for (int i=0; i<f_n; i++) {
        f_elems[i] = *(elems.begin() + i);
    }
}

bool Vector::operator==(Vector v) {
    if (f_n != v.f_n) return false;
    for (int i=0; i<f_n; i++) {
        if (f_elems[i] != v.f_elems[i]) return false;
    }
    return true;
}

bool Vector::operator!=(Vector v) {
    return !(*this==v);
}

Vector Vector::operator+(Vector v) {    // TODO: add checks for vectors of same size
    int nums[f_n];
    for (int i=0; i<f_n; i++) {
        nums[i] = f_elems[i] + v.f_elems[i];
    }
    return Vector(f_n, nums);
}

Vector Vector::operator-(Vector v) {
    int nums[f_n];
    for (int i=0; i<f_n; i++) {
        nums[i] = f_elems[i] - v.f_elems[i];
    }
    return Vector(f_n, nums);
}

int Vector::operator*(Vector v) {
    int sum = 0;
    for (int i=0; i<f_n; i++) {
        sum += f_elems[i] * v.f_elems[i];
    }
    return sum;
}

int Vector::index(int i) {
    return f_elems[i];
}

void printVector(Vector v, bool even_spacing) {

    if (even_spacing) {
        int widths[v.f_n];
        for (int i=0; i<v.f_n; i++) {
            widths[i] = num_digits(v.f_elems[i]) + 1;
        } 
        int width = max(widths, v.f_n);

        printf("[");
        for (int i=0; i<v.f_n; i++) {
            printf("%*d", width, v.f_elems[i]);
        }
        printf(" ]");
    }
    
    else {
        printf("[");
        for (int i=0; i<v.f_n; i++) {
            printf(" %d", v.f_elems[i]);
        }
        printf(" ]");
    }
    
}

