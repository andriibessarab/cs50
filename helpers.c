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
            image[i][j].rgbtRed = round((float) avgR / l);
            image[i][j].rgbtGreen = round((float) avgG / l);
            image[i][j].rgbtBlue = round((float) avgB / l);
        }
    }
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
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
            // Delcare var's for holding values of R, G, B, of 9 elements
            int valR[3][3] = {{0, 0, 0}, {0, 0, 0}, {0, 0, 0}};
            int valG[3][3] = {{0, 0, 0}, {0, 0, 0}, {0, 0, 0}};
            int valB[3][3] = {{0, 0, 0}, {0, 0, 0}, {0, 0, 0}};

            // Find out the avg values of R, G, B

            /**
             * 00  01  02
             * 10  11  12
             * 20  21  22
             */

            // 11(curr. element)
            valR[1][1] = image_copy[i][j].rgbtRed;
            valG[1][1] = image_copy[i][j].rgbtGreen;
            valB[1][1] = image_copy[i][j].rgbtBlue;

            // First row(00, 01, 02)
            if (i != 0)
            {
                // 00
                if (j != 0)
                {
                    valR[0][0] = image_copy[i - 1][j - 1].rgbtRed;
                    valG[0][0] = image_copy[i - 1][j - 1].rgbtGreen;
                    valB[0][0] = image_copy[i - 1][j - 1].rgbtBlue;
                }

                // 01
                valR[0][1] = image_copy[i - 1][j].rgbtRed;
                valG[0][1] = image_copy[i - 1][j].rgbtGreen;
                valB[0][1] = image_copy[i - 1][j].rgbtBlue;

                // 02
                if (j != width - 1)
                {
                    valR[0][2] = image_copy[i - 1][j + 1].rgbtRed;
                    valG[0][2] = image_copy[i - 1][j + 1].rgbtGreen;
                    valB[0][2] = image_copy[i - 1][j + 1].rgbtBlue;
                }
            }

            // Middle row(10, 12)

            // 10
            if (j != 0)
            {
                valR[1][0] = image_copy[i][j - 1].rgbtRed;
                valG[1][0] = image_copy[i][j - 1].rgbtGreen;
                valB[1][0] = image_copy[i][j - 1].rgbtBlue;
            }

            // 12
            if (j != width - 1)
            {
                valR[1][2] = image_copy[i][j + 1].rgbtRed;
                valG[1][2] = image_copy[i][j + 1].rgbtGreen;
                valB[1][2] = image_copy[i][j + 1].rgbtBlue;
            }

            // Last row(20, 21, 22)
            if (i != height - 1)
            {
                // 20
                if (j != 0)
                {
                    valR[2][0] = image_copy[i + 1][j - 1].rgbtRed;
                    valG[2][0] = image_copy[i + 1][j - 1].rgbtGreen;
                    valB[2][0] = image_copy[i + 1][j - 1].rgbtBlue;
                }

                // 21
                valR[2][1] = image_copy[i + 1][j].rgbtRed;
                valG[2][1] = image_copy[i + 1][j].rgbtGreen;
                valB[2][1] = image_copy[i + 1][j].rgbtBlue;

                // 22
                if (j != width - 1)
                {
                    valR[2][2] = image_copy[i + 1][j + 1].rgbtRed;
                    valG[2][2] = image_copy[i + 1][j + 1].rgbtGreen;
                    valB[2][2] = image_copy[i + 1][j + 1].rgbtBlue;
                }
            }

            // Find Gx and Gy for R, G, B
            int GxR = (valR[0][0] * -1) + (valR[0][1] * 0) + (valR[0][2] * 1)
                    + (valR[1][0] * -2) + (valR[1][1] * 0) + (valR[1][2] * 2)
                    + (valR[2][0] * -1) + (valR[2][1] * 0) + (valR[2][2] * 1);

            int GxG = (valG[0][0] * -1) + (valG[0][1] * 0) + (valG[0][2] * 1)
                    + (valG[1][0] * -2) + (valG[1][1] * 0) + (valG[1][2] * 2)
                    + (valG[2][0] * -1) + (valG[2][1] * 0) + (valG[2][2] * 1);

            int GxB = (valB[0][0] * -1) + (valB[0][1] * 0) + (valB[0][2] * 1)
                    + (valB[1][0] * -2) + (valB[1][1] * 0) + (valB[1][2] * 2)
                    + (valB[2][0] * -1) + (valB[2][1] * 0) + (valB[2][2] * 1);

            int GyR = (valR[0][0] * -1) + (valR[0][1] * -2) + (valR[0][2] * -1)
                    + (valR[1][0] *  0) + (valR[1][1] *  0) + (valR[1][2] *  0)
                    + (valR[2][0] *  1) + (valR[2][1] *  2) + (valR[2][2] *  1);

            int GyG = (valG[0][0] * -1) + (valG[0][1] * -2) + (valG[0][2] * -1)
                    + (valG[1][0] *  0) + (valG[1][1] *  0) + (valG[1][2] *  0)
                    + (valG[2][0] *  1) + (valG[2][1] *  2) + (valG[2][2] *  1);

            int GyB = (valB[0][0] * -1) + (valB[0][1] * -2) + (valB[0][2] * -1)
                    + (valB[1][0] *  0) + (valB[1][1] *  0) + (valB[1][2] *  0)
                    + (valB[2][0] *  1) + (valB[2][1] *  2) + (valB[2][2] *  1);

            // Get values of R, G B
            int red = round(sqrt(pow(GxR, 2) + pow(GyR, 2)));
            int green = round(sqrt(pow(GxG, 2) + pow(GyG, 2)));
            int blue = round(sqrt(pow(GxB, 2) + pow(GyB, 2)));

            // Set value of R
            if (red > 255)
            {
                image[i][j].rgbtRed = 255;
            }
            else
            {
                image[i][j].rgbtRed = red;
            }

            // Set value of G
            if (green > 255)
            {
                image[i][j].rgbtGreen = 255;
            }
            else
            {
                image[i][j].rgbtGreen = green;
            }

            // Set value of B
            if (blue > 255)
            {
                image[i][j].rgbtBlue = 255;
            }
            else
            {
                image[i][j].rgbtBlue = blue;
            }
        }
    }
}