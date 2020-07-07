#include <stdio.h>
#include <cs50.h>
#include <string.h>

int main(void)
{

    //Get text
    string text = get_string("Text: ");

    //Declare variables
    float letters = 0;
    int words = 1;
    float sentences = 0;

    //Get number of letters, words, sentences
    for (int i = 0; i < strlen(text); i++)
    {
        //Check if i is a letter
        if ((text[i] >= 65 && text[i] <= 90) || (text[i] >= 97 && text[i] <= 122))
        {
            letters++;
        }

        //Check if i ends the word(space)
        if (text[i] == 32 && text[i + 1] != 32)
        {
            words++;
        }

        //Check if i ends the sentence(. or ! or ?)
        if (text[i] == 46 || text[i] == 33 || text[i] == 63)
        {
            sentences++;
        }
    }

    //Find out the number of letters and sentences per 100 words
    letters *= (float) 100 / words;
    sentences *= (float) 100 / words;

    //Find out the text's readability using Coleman-Liau index formula
    float index = 0.0588 * letters - 0.296 * sentences - 15.8;

    //Print out the results
    if (index >= 1 && index <= 16)
    {
        printf("Grade: %.0f\n", index);
    }
    else if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else
    {
        printf("Grade 16+\n");
    }
}