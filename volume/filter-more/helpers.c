#include "helpers.h"
#include <math.h>


// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0 ; i < height ; i++)
    {
        for (int j = 0  ; j < width ; j++)
        {
            RGBTRIPLE pixel = image[i][j];
            float real_avg = (pixel.rgbtRed + pixel.rgbtGreen + pixel.rgbtBlue) / 3.000;
            int average = round(real_avg);

            image[i][j].rgbtRed = average;
            image[i][j].rgbtBlue = average;
            image[i][j].rgbtGreen = average;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for(int i = 0 ; i < height ; i++)
    {
        for (int j = 0 ; j < width / 2 ; j++)
        {
            RGBTRIPLE tmp = image[i][j] ;
            image[i][j] = image[i][width - j - 1];
            image[i][width - j - 1] = tmp;
        }
    }
    return;
}


RGBTRIPLE neighbors_avg(int height, int width, int i, int j, RGBTRIPLE image[height][width])
{
    RGBTRIPLE pixel;
    float red = 0;
    float green = 0;
    float blue = 0;
    float number = 0; //number of neighbors
    for (int k = -1 ; k < 2; k++)
    {
        for (int l = -1; l < 2; l++)
        {
            if ((i + k >= 0) && (j + l >= 0) && (i + k < height) && (j + l < width))
            {
                red += image[i + k][j + l].rgbtRed;
                green += image[i + k][j + l].rgbtGreen;
                blue += image[i + k][j + l].rgbtBlue;
                number += 1;
            }
        }
    }
    pixel.rgbtRed = round(red / number);
    pixel.rgbtGreen = round (green / number);
    pixel.rgbtBlue = round (blue / number);
    return pixel;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE temp[height][width];
    for (int i = 0 ; i < height ; i ++)
    {
        for(int j = 0 ; j < width ; j++)
        {
            temp[i][j] = neighbors_avg(height, width, i ,j, image);
        }
    }

    for (int i = 0 ; i < height; i++)
    {
        for (int j = 0 ; j < width; j++)
        {
            image[i][j] = temp[i][j];
        }
    }
    return;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE temp[height][width];
    int gx[3][3] = {{-1 , 0 ,1} , {-2 , 0 , 2} , {-1 , 0 , 1}};
    int gy[3][3] = {{-1 , -2 , -1} , {0 , 0 , 0} , {1 , 2 , 1}};
    for (int i = 0 ; i < height ; i++)
    {
        for(int j = 0 ; j < width ; j++)
        {
            int x_red = 0;
            int x_green = 0;
            int x_blue = 0;
            int y_red = 0;
            int y_green = 0;
            int y_blue = 0;
            for(int k = -1 ; k < 2 ; k++)
            {
                for(int l = -1 ; l < 2 ; l++)
                {
                    int gx_value = gx[k + 1][l + 1];
                    int gy_value = gy[k + 1][l + 1];
                    if (!((i + k >= 0) && (j + l >= 0) && (i + k < height) && (j + l < width)))
                    {
                        gx_value = 0;
                        gy_value = 0;
                    }
                    x_red += image[i + k][j + l].rgbtRed * gx_value;
                    x_green += image[i + k][j + l].rgbtGreen * gx_value;
                    x_blue += image[i + k][j + l].rgbtBlue * gx_value;
                    y_red += image[i + k][j + l].rgbtRed * gy_value;
                    y_green += image[i + k][j + l].rgbtGreen * gy_value;
                    y_blue += image[i + k][j + l].rgbtBlue * gy_value;
                }
            }
            int red = round(sqrt((x_red * x_red) + (y_red * y_red)));
            if (red > 255)
            {
                red = 255;
            }
            temp[i][j].rgbtRed = red;
            int green = round(sqrt((x_green * x_green) + (y_green * y_green)));
            if (green > 255)
            {
                green = 255;
            }
            temp[i][j].rgbtGreen = green;
            int blue = round(sqrt((x_blue * x_blue) + (y_blue * y_blue)));
            if (blue > 255)
            {
                blue = 255;
            }
            temp[i][j].rgbtBlue = blue;
        }
    }
    for (int i = 0 ; i < height ; i++)
    {
        for(int j = 0 ; j < width ; j++)
        {
            image[i][j] = temp[i][j];
        }
    }
}
