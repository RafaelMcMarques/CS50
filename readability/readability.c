#include <cs50.h>
#include <stdio.h>
#include<string.h>
#include<math.h>

//count letters words and sentences
int count_letters(string s);
int count_words(string s);
int count_sentences(string s);
int main(void)
{
    string s = get_string("Text: ");
    float L = (float)count_letters(s) / (float)count_words(s) * 100;
    float S = (float)count_sentences(s) / (float)count_words(s) * 100;
    int index = round(0.0588 * L - 0.296 * S - 15.8);
    if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (index > 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %d\n" , index);
    }
    return 0;
}

int count_letters(string s)
{
    int letters = 0;
    for (int i = 0 ; i < strlen(s) ; i++)
    {
        if ((s[i] >= 65 && s[i] <= 90) || (s[i] >= 97 && s[i] <= 122))
        {
            letters ++;
        }
    }
    return letters;
}

int count_words(string s)
{
    int words = 0;
    for (int i = 0 ; i < strlen(s) ; i++)
    {
        if(s[i] == 32)
        {
            words ++;
        }
    }
    return words + 1;
}

int count_sentences(string s)
{
    int sentences = 0;
    for (int i = 0 ; i < strlen(s) ; i++)
    {
        if (s[i] == '.' || s[i] == '!' || s[i] == '?')
        {
            sentences++;
        }
    }
    return sentences;
}