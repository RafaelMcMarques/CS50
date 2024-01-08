#include<cs50.h>
#include<stdio.h>

int main(void){
    int preferences[2][5] = {{0,1,2,3,4} , {5,6,7,8,9}};
    preferences[1][0] = 7;
    printf("%d" , preferences[1][0]);

}