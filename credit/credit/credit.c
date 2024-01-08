#include <cs50.h>
#include <stdio.h>


//INTERMINADO

int check(int card_number)
{
    int sum = 0;
    int i = 0;
    while (card_number > 0)
    {
        int digit = card_number % 10;
        card_number = card_number / 10;

        if ((i % 2)  == 0)
        {
            sum = sum + digit;
        }
        else
        {
            sum = sum + (digit * 2);
        }
        i++;
    }

    return ((sum % 10) == 0);
}

int get_len(int number)
{
    int len = 0;
    while (number > 0)
    {
        number = number / 10;
        len++;
    }
    return len;
}

void print_output(card_number)
{
    int len = get_len(card_number);

}

int main(void)
{
    long card_number = 0;
    while (card_number != 0)
    {
        card_number = get_long("");
    }

    if (check(card_number) == 1)
    {
        print_output(card_number);
        return 0;
    }
    printf("INVALID\n");
}