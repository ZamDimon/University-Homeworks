#include <stdio.h>
#include <stdlib.h>
#include <time.h>

void fillRandom(int* array, int n, int m)
{
    srand(time(0));
    for (int i = 0; i < n*m; ++i)
    {
        *(array + i) = rand();
    }
}

void printArray(int* array, int n, int m)
{
    for (int i = 0; i < m; ++i)
    {
        for (int j = 0; j < n; ++j)
        {
            printf("%d ", *(array + i*n + j));
        }
        printf("\n");
    }
}

int main(int argc, char *argv[])
{
    // Define numbers n and m
    int n, m;
    // Read numbers n and m
    printf("Type in number N: ");
    scanf("%d", &n);
    printf("Type in number M: ");
    scanf("%d", &m);

    /*
     * Allocate memory to the array
     * Note: here we will represent the two-dimensional array using a single pointer of size n*m*sizeof(int)
     * Another ways how we could have defined two-dimensional array:
     * 1) using double pointer (int**)
     * 2) array of pointers (int* array[size])
     */

    // Allocate memory. We should allocate n*m "cells" with sizeof(int) bytes in each
    int* dynamicArray = malloc((n*m) * sizeof(int));

    if (dynamicArray == NULL)
    {
        printf("Failed to allocate memory\n");
        return 0;
    }

    // Filling the array with random numbers
    fillRandom(dynamicArray, n, m);

    // Printing the array in a form of matrice
    printArray(dynamicArray, n, m);

    // Do not waste memory!
    free(dynamicArray);

    return 0;
}
