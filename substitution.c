#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>

int main(int argc, string argv[])
{
    //Validate key

    //Check if user provided key
    if (argc != 2)
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }

    //Check if key is 26 char. long
    if (strlen(argv[1]) != 26)
    {
        printf("Key must contain 26 characters.\n");
        return 1;
    }

    for (int i = 0; i < strlen(argv[1]); i++)
    {

        //Check if each char. is a letter
        if (!isalpha(argv[1][i]))
        {
            printf("Key must only contain alphabetic characters.\n");
            return 1;
        }

        //Check for repeated characters
        for (int n = 0; n < strlen(argv[1]); n++)
        {
            if (i != n && argv[1][i] == argv[1][n])
            {
                printf("Key must not contain repeated characters.\n");
                return 1;
            }
        }
    }

    //Get plaintext
    string text = get_string("plaintext: ");

    //Enchipher text
    for (int i = 0; i < strlen(text); i++)
    {
        if (isalpha(text[i]))
        {
            if (isupper(text[i]))
            {
                text[i] = toupper(argv[1][text[i] - 65]);
            }
            else
            {
                text[i] = tolower(argv[1][text[i] - 97]);
            }
        }
    }


    //Print ciphertext
    printf("ciphertext: %s\n", text);
}