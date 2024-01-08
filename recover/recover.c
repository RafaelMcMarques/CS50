#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

typedef uint8_t BYTE;

int check_new(BYTE buffer[]);

int main(int argc, char *argv[])
{
    if(argc != 2)
    {
        printf("Usage: ./recover IMAGE");
        return 1;
    }

    FILE *card = fopen(argv[1] , "r");

    BYTE buffer[512];
    int i = 0;
    int found = 0;
    FILE *new_jpg;
    char jpeg[7];

    while (fread(buffer , 512 , 1 , card) != 0)
    {
        if (check_new(buffer) == 1)
        {
            if (found == 1)
            {
                fclose(new_jpg);
            }
            found = 1;
            sprintf(jpeg , "%03i.jpg" , i);
            new_jpg = fopen(jpeg , "w");
            fwrite(buffer , 512 , 1 , new_jpg);
            i++;
        }
        else if(found == 1)
        {
            fwrite(buffer , 512 , 1 , new_jpg);
        }
    }
    fclose(new_jpg);
    fclose(card);
}

int check_new(BYTE buffer[])
{
    if(buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
    {
        return 1;
    }
    return 0;
}