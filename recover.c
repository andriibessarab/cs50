#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    // Check if user provided name of memory card
    if (argc != 2)
    {
        printf("Usage: ./recover image\n");
        return 1;
    }

    // Open a memory card
    FILE *card = fopen(argv[1], "r");

    // Check if file opened properly
    if (card == NULL)
    {
        printf("Could not open %s\n", argv[1]);
        return 1;
    }
    
    // Declare neccessary variables
    unsigned char buffer[512];
    int img_counter = 0;
    char img_name[8];
    FILE *img;

    // Recover images
    while (fread(buffer, sizeof(char), sizeof(buffer), card) == sizeof(buffer))
    {

        // Check if curr chunk is beginning of img
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            // If it's not a first img, then close prev img
            if (img_counter != 0)
            {
                fclose(img);
            }

            // Create a new img
            sprintf(img_name, "%03i.jpg", img_counter);
            img_counter++;
            img = fopen(img_name, "a");
            fwrite(&buffer, sizeof(char), sizeof(buffer), img);
        }
        else
        {
            // If method = write, then append curr chunk to img
            if (img_counter != 0)
            {
                fwrite(&buffer, sizeof(char), sizeof(buffer), img);
            }
        }
    }
}