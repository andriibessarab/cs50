#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // Get the avg of R, G, B
            int avg = round((image[i][j].rgbtRed + image[i][j].rgbtGreen + image[i][j].rgbtBlue) / 3.0);

            // Set all values equal to avg
            image[i][j].rgbtRed = avg;
            image[i][j].rgbtBlue = avg;
            image[i][j].rgbtGreen = avg;
        }
    }
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width / 2; j++)
        {
            // Remember value of image[i][j]
            RGBTRIPLE a = image[i][j];

            // Switch px's in the right part and in the left part of the row
            image[i][j] = image[i][width - (j + 1)];
            image[i][width - (j + 1)] = a;
        }
    }
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    //Make a copy of an image
    RGBTRIPLE image_copy[height][width];

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image_copy[i][j] = image[i][j];
        }
    }

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // Delcare var's for avg values of R, G, B, and elements count
            int l = 0;
            int avgR = 0;
            int avgG = 0;
            int avgB = 0;
            
            // Find out the avg values of R, G, B

            /**
             * 1  2  3
             * 4  #  5
             * 6  7  8
             */

            // #
            l++;
            avgR += image_copy[i][j].rgbtRed;
            avgG += image_copy[i][j].rgbtGreen;
            avgB += image_copy[i][j].rgbtBlue;

            // First row(1, 2, 3)
            if (i != 0)
            {
                // 1
                if (j != 0)
                {
                    l++;
                    avgR += image_copy[i - 1][j - 1].rgbtRed;
                    avgG += image_copy[i - 1][j - 1].rgbtGreen;
                    avgB += image_copy[i - 1][j - 1].rgbtBlue;
                }

                // 2
                l++;
                avgR += image_copy[i - 1][j].rgbtRed;
                avgG += image_copy[i - 1][j].rgbtGreen;
                avgB += image_copy[i - 1][j].rgbtBlue;
                
                // 3
                if (j != width - 1)
                {
                    l++;
                    avgR += image_copy[i - 1][j + 1].rgbtRed;
                    avgG += image_copy[i - 1][j + 1].rgbtGreen;
                    avgB += image_copy[i - 1][j + 1].rgbtBlue;
                }
            }
            
            // Middle(4, 5)

            // 4
            if (j != 0)
            {
                l++;
                avgR += image_copy[i][j - 1].rgbtRed;
                avgG += image_copy[i][j - 1].rgbtGreen;
                avgB += image_copy[i][j - 1].rgbtBlue;
            }

            // 5
            if (j != width - 1)
            {
                l++;
                avgR += image_copy[i][j + 1].rgbtRed;
                avgG += image_copy[i][j + 1].rgbtGreen;
                avgB += image_copy[i][j + 1].rgbtBlue;
            }
            
            // Last Row(6, 7, 8)
            if (i != height - 1)
            {
                // 6
                if (j != 0)
                {
                    l++;
                    avgR += image_copy[i + 1][j - 1].rgbtRed;
                    avgG += image_copy[i + 1][j - 1].rgbtGreen;
                    avgB += image_copy[i + 1][j - 1].rgbtBlue;
                }

                // 7
                l++;
                avgR += image_copy[i + 1][j].rgbtRed;
                avgG += image_copy[i + 1][j].rgbtGreen;
                avgB += image_copy[i + 1][j].rgbtBlue;
                
                // 8
                if (j != width - 1)
                {
                    l++;
                    avgR += image_copy[i + 1][j + 1].rgbtRed;
                    avgG += image_copy[i + 1][j + 1].rgbtGreen;
                    avgB += image_copy[i + 1][j + 1].rgbtBlue;
                }
            }

            // Set R, G, B values to the pixel
            image[i][j].rgbtRed = floor((float) avgR / l);
            image[i][j].rgbtGreen = floor((float) avgG / l);
            image[i][j].rgbtBlue = floor((float) avgB / l);
        }
    }
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    return;
}