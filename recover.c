#include <stdio.h>
#include <stdlib.h>

void read_chunk(FILE *card, char method, FILE *img);
int i = 0;

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

    // Start reading a card by chunks
    read_chunk(card, 'f', NULL);
}

void read_chunk(FILE *card, char method, FILE *img)
{
    // Creat a buffer to store information
    unsigned char buffer[512];
    
    // Check if didn't reach the end of file
    if (fread(buffer, sizeof(char), sizeof(buffer), card) != sizeof(buffer))
    {
        if (img != NULL)
        {
            fclose(img);
        }
        fclose(card);
        return;
    }
    else
    {
        // Check if curr chunk is beginning of img
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            // If method = write, then close prev img and set method to find
            if (method == 'w')
            {
                fclose(img);
                method = 'f';
            }
            // If method = find, then start a new image
            if (method == 'f')
            {
                char img_name[8];
                sprintf(img_name, "%03i.jpeg", i);
                i++;
                FILE *new_img = fopen(img_name, "a");
                fwrite(buffer, sizeof(char), sizeof(buffer), new_img);
                read_chunk(card, 'w', new_img);
                return;
            }
        }
        else
        {
            // If method = write, then append curr chunk to img
            if (method = 'w')
            {
                fwrite(buffer, sizeof(char), sizeof(buffer), img);
                read_chunk(card, 'w', img);
                return;
            }

            // Else keep looking for img
            read_chunk(card, 'f', NULL);  
        }
    }
}