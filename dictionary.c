// Implements a dictionary's functionality

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <strings.h>
#include <ctype.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Declare functions
void del_list(node *n);

// Number of buckets in hash table
const unsigned int N = 27;

//Words counter
int word_counter = 0;

// Hash table
node *table[N];

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    int index = hash(word);
    node *tmp = table[index];

    while (tmp != NULL)
    {
        if (strcasecmp(word, tmp->word) == 0)
        {
            return true;
        }
        tmp = tmp->next;
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    if (isalpha(word[0]))
    {
        return toupper(word[0]) - 65;
    }
    else
    {
        return 26;
    }
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    // Open dictionary file
    FILE *dict = fopen(dictionary, "r");
    if (dict == NULL)
    {
        return false;
    }

    // Read strings from file one at a time
    char *word = malloc(sizeof(char) * LENGTH);
    if (word == NULL)
    {
        return false;
    }

    // Create a new node for each word
    while (fscanf(dict, "%s", word) != EOF)
    {
        word_counter++;

        node *n = malloc(sizeof(node));
        if (n == NULL)
        {
            return false;
        }

        strcpy(n->word, word);

        // Hash word to obtain a hash value
        int index = hash(word);

        // Insert node into hash table at that location
        n->next = table[index];
        table[index] = n;
    }

    fclose(dict);
    free(word);

    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    return word_counter;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    for (int i = 0; i < N; i++)
    {
        if (table[i] != NULL)
        {
            del_list(table[i]);
        }
    }
    return true;
}

// Delete elements from linked list
void del_list(node *n)
{
    if (n->next == NULL)
    {
        free(n);
        return;
    }
    del_list(n->next);
    free(n);
}