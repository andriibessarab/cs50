#include <stdio.h>
#include <cs50.h>


bool checksum(long card);
int length(long card);
int digits(int num, long card);


int main(void)
{
    //Getting user's card's number
    long card = get_long("Credit Card Number:");

    //Checking if the card is valid
    if (checksum(card))
    {
        //Check if the card is AMEX
        if (length(card) == 15 && (digits(2, card) == 34 || digits(2, card) == 37))
        {
            printf("AMEX\n");
        }

        //Check if the card is MASTERCARD
        else if (length(card) == 16 && (digits(2, card) >= 51 && digits(2, card) <= 55))
        {
            printf("MASTERCARD\n");
        }
        //Check if the card is VISA
        else if ((length(card) == 13 || length(card) == 16) && digits(1, card) == 4)
        {
            printf("VISA\n");
        }
        else
        {
            printf("INVALID\n");
        }
    }
    else
    {
        printf("INVALID\n");
    }
}


//Checksum function
bool checksum(long card)
{
    int total = 0;

    //Multipling every other digit by 2, and adding them to total.
    for (long i = card / 10; i > 0; i /= 100)
    {
        long n = i % 10 * 2;
        if (n >= 10)
        {
            total += n / 10;
            total += n % 10;
        }
        else
        {
            total += n;
        }
    }

    //Adding the sum of the digits that weren’t multiplied by 2 to total
    for (long i = card; i > 0; i /= 100)
    {
        total += i % 10;
    }

    //Check if card is valid
    if (total % 10 == 0)
    {
        return true;
    }
    else
    {
        return false;
    }
}

//Card's length function
int length(long card)
{
    int length = 0;
    do
    {
        length++;
        card /= 10;
    }
    while (card > 0);

    return length;
}

//First two digits function
int digits(int num, long card)
{
    for (int i = length(card) - num; i > 0; i--)
    {
        card /= 10;
    }
    return card;
}