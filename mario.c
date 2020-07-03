#include <stdio.h>
#include <cs50.h>

int get_height();

int main(void)
{

    //Get height
    int height = get_height();

    //Print pyramids by rows
    for (int row = 1; row <= height; row++)
    {
        //Print spaces before the bricks
        for (int i = 1; i <= height - row; i++)
        {
            printf(" ");
        }

        //Print left pyramid's bricks
        for (int i = 1; i <= row; i++)
        {
            printf("#");
        }

        //Print spaces between left and right pyramids
        printf("  ");

        //Print right pyramid's bricks
        for (int i = 1; i <= row; i++)
        {
            printf("#");
        }

        //Go to a new line
        printf("\n");
    }
}

//Get height function
int get_height(void)
{
    while (true)
    {
        //Get height
        int height = get_int("Height: ");

        //Check if height is between 1 and 8
        if (height >= 1 && height <= 8)
        {
            return height;
        }
    }
}