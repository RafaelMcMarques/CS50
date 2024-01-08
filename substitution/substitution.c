#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>

bool check_key(string key);
void print_ciphertext(string plaintext , string key);

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./substitution key. \n");
        return 1;
    }

    string key = argv[1];

    if(!(check_key(key)))
    {
        printf("Key must contain 26 distinct alphabetical digits. \n");
        return 1;
    }
    string plaintext = get_string("plaintext: ");
    print_ciphertext(plaintext , key);
    return 0;
}

bool duplicate(string key)
{


    for (int i = strlen(key) - 1; i >= 0; i--)
    {
        for (int j = 0 ; j < i ; j++)
        {
            if (key[i] == key[j])
            {
                return false;
            }
        }
    }
    return true;
}

bool check_key(string key)
{
    if (strlen(key) != 26)
    {
        return false;
    }




    for(int i = 0 ; i < 26 ; i++)
    {
        if (!(isalpha(key[i])))
        {
            return false;
        }
        for (int j = 0; j < i; j++)
        {
            if (key[i] == key[j])
            {
                return false;
            }
        }
    }
    return true;
}



void print_ciphertext(string plaintext , string key)
{
    printf("ciphertext: ");
    for (int i = 0 ; i < strlen(plaintext) ; i++)
    {
        int pos_key;
        char encripted_char;
        if (isupper(plaintext[i]))
        {
            pos_key = plaintext[i] - 65;
            encripted_char = key[pos_key];
            if (islower(encripted_char))
            {
                encripted_char -= 32;
            }
        }

        else if(islower(plaintext[i]))
        {
            pos_key = plaintext[i] - 97;
            encripted_char = key[pos_key];
            if (isupper(encripted_char))
            {
                encripted_char += 32;
            }
        }

        else
        {
            encripted_char = plaintext[i];
        }

    printf("%c" , encripted_char);
    }

printf("\n");
}


