#pragma once

int log(int b, int n) {
    int count = 0;
    int mult = 1;
    while (n > mult) {
        mult *= b;
        count++;
    }
    return count;
}

int num_digits(int n) {
    if (!n) return 1;
    return log(10, n+1);
}

int max(int nums[], int n) {
    int curr = nums[0];
    for (int i=1; i<n; i++) {
        if (nums[i] > curr) {
            curr = nums[i];
        }
    }
    return curr;
}
