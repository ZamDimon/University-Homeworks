#include <stdio.h>
#include <string.h>
#include <ctype.h>

#define MAX_STRING_SIZE 100

// For task 2
void printStringLength(char string[MAX_STRING_SIZE])
{
    printf("Length of %s is %d\n", string, strlen(string));
}

// For task 6
int hasDigit(char string[MAX_STRING_SIZE])
{
    for (int i = 0; i < strlen(string); ++i)
    {
        if (isdigit(string[i]))
            return 1;
    }

    return 0;
}

int main () 
{
	// Initializing variables
	char string1[MAX_STRING_SIZE] = "";
	char string2[MAX_STRING_SIZE] = "";
	int n1, n2; //Used for task 7

	// Reading the input (Task 1)
	printf("Write down the first string: ");
	gets(string1);

	printf("Write down the second string: ");
	gets(string2);

	printf("Write down an integer n1: ");
	scanf("%d", &n1);

    printf("Write down an integer n2: ");
    scanf("%d", &n2);

	// Printing the strings lengths (Task 2)
    printStringLength(string1);
    printStringLength(string2);

    // Copying s1 into string1_copy and s2 into string2_copy(Task 3)
    char string1_copy[MAX_STRING_SIZE], string2_copy[MAX_STRING_SIZE];
    strcpy(string1_copy, string1);
    strcpy(string2_copy, string2);
    printf("String 1 copy is %s\n", string1_copy);
    printf("String 2 copy is %s\n", string2_copy);

    // Copying first n1 symbols of string1_copy into string1_copy_k (Task 4)
    char string1_copy_k[MAX_STRING_SIZE];
    if (n1 > strlen(string1_copy))
        printf("n1 is larger than the length of string1_copy\n");
    else
    {
        strncpy(string1_copy_k, string1_copy, n1);
        printf("string1_copy_k is %s\n", string1_copy_k);
    }

    // Adding string1 and string2 and writing the result to string3 (Task 5)
    char string3[MAX_STRING_SIZE];
    strcpy(string3, strcat(string1_copy, string2_copy));
    printf("string 3 is %s\n", string3);

    // Checking whether string3 has a digit (Task 6)
    int has_digit = hasDigit(string3);
    printf(has_digit? "string3 contains a digit\n" : "string3 does not contain a digit\n");

    // Task 7
    char substring[MAX_STRING_SIZE];
    if (n2 <= n1)
        printf("n2 must be greater than n1");
    else {
        strncpy(substring, &string3[n1-1], n2 - n1 + 1);
        printf("Substring of string3 from %d to %d including is %s\n", n1, n2, substring);
    }

	return 0;
}
