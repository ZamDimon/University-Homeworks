#include <stdio.h>
#include <string.h>
#include <ctype.h>

#define MAX_STRING_SIZE 50

char* remove_spaces(char* text)
{
    int i = 0, j = 0;
    while (text[j] != '\0')
    {
        if(text[i] != ' ')
            text[j++] = text[i];

        i++;
    }
    text[j] = '\0';
    return text;
}

int main()
{
    char text[MAX_STRING_SIZE] = "";
    printf("Print your string: ");
    gets(text);
    remove_spaces(text);
    printf("String without spaces: %s", text);

    return 0;
}
