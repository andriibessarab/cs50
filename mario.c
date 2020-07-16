#include <stdio.h>
#include <cs50.h>

void get_height(void);
void print_row(int len);

int height;

int main(void)
{
    //Get height
    get_height();

    //Print pyramid
    print_row(height);
}


//Get height function
void get_height(void)
{
    //Get height
    height = get_int("Height: ");

    //Check if height is between 1 and 8
    if (!(height >= 1 && height <= 8))
    {
        get_height();
    }
}

void print_row(int len)
{
    //Return if len of row is 0
    if (len == 0)
    {
        return;
    }

    //Print shorter row first
    print_row(len - 1);

    //Print spaces
    for (int i = 0; i < height - len; i++)
    {
        printf(" ");
    }

    //Print bricks
    for (int i = 0; i < len; i++)
    {
        printf("#");
    }
    printf("\n");
}