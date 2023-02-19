#include <stdio.h>
#include <stdlib.h>

// Define arithmetic mean function
float arithmeticMean(float *array, int arraySize)
{
    float sum = 0.0f;
    for (int i = 0; i < arraySize; ++i)
        sum += *(array + i);

    return sum / (float)arraySize;
}

// Define harmonic mean function
float harmonicMean(float *array, int arraySize)
{
    float inverseSum = 0.0f;
    for (int i = 0; i < arraySize; ++i)
        inverseSum += 1/(*(array + i));

    return (float)arraySize/inverseSum;
}

int main(int argc, char *argv[])
{
    // Define and read the size of an array
    int numberOfElements;
    printf("Number of elements: ");
    scanf("%d", &numberOfElements);

    // Allocate memory to an array
    float *dynamicArray = (float*)malloc(numberOfElements * sizeof(float));

    // Read array
    for (int i = 0; i < numberOfElements; ++i)
    {
        printf("Type in number %d: ", i+1);
        scanf("%f", dynamicArray+i);
    }

    // Print the result
    printf("Arithmetic mean of the array is %f\n", arithmeticMean(dynamicArray, numberOfElements));
    printf("Harmonic mean of the array is %f\n", harmonicMean(dynamicArray, numberOfElements));

    // Do not waste memory!!!
    free(dynamicArray);
}
