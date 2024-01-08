#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int size = 0;
    while ((size <= 0) || (size >= 9))
    {
        size = get_int("Height: ");
    }

    for (int i = 0; i < size ; i++)
    {
        for (int j = 1 ; j < (size - i); j++)
        {
            printf(" ");
        }
        for (int j = 0; j <= i; j++)
        {
            printf("#");
        }
        printf("  ");
        for (int j = 0; j <= i; j++)
        {
            printf("#");
        }
        printf("\n");
    }
}