#include <stdlib.h>
#include "sequence.h"

// generate all numbers that look like 2^p * 3^q and are less than n
// return them sorted ascending in a array
long *Generate_2p3q_Seq(int n, int *seq_size)
{
    if (n <= 1) {
        *seq_size = 0;
        return malloc(0);
    }

    // first pass just counts how many there are
    int count = 0;
    long pow2 = 1;
    while (pow2 < n) {
        long val = pow2;
        while (val < n) {
            count++;
            val *= 3;
        }
        pow2 *= 2;
    }

    long *seq = malloc(count * sizeof(long));
    if (seq == NULL) {
        *seq_size = 0;
        return NULL;
    }

    // second pass fills them in
    int idx = 0;
    pow2 = 1;
    while (pow2 < n) {
        long val = pow2;
        while (val < n) {
            seq[idx++] = val;
            val *= 3;
        }
        pow2 *= 2;
    }

    // sort them, just a basic insertion sort since theres too many
    for (int i = 1; i < count; i++) {
        long tmp = seq[i];
        int j = i - 1;
        while (j >= 0 && seq[j] > tmp) 
        {
            seq[j + 1] = seq[j];
            j--;
        }
        seq[j + 1] = tmp;
    }

    *seq_size = count;
    return seq;
}
