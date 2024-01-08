#include<stdio.h>
#include<cs50.h>

typedef struct
{
    int looser;
    int winner;
}
pairs;

int main(void)
{
    pairs pairs[2];
    pairs[0].looser = 1;
    pairs[0].winner = 2;
    pairs[1] = pairs[0];
    printf("%d" , pairs[1].winner);

}