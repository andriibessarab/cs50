#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

// Max number of candidates
#define MAX 9

// Candidates have name and vote count
typedef struct
{
    string name;
    int votes;
}
candidate;

// Array of candidates
candidate candidates[MAX];

// Number of candidates
int candidate_count;

// Function prototypes
bool vote(string name);
void print_winner(void);

int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: plurality [candidate ...]\n");
        return 1;
    }

    // Populate array of candidates
    candidate_count = argc - 1;
    if (candidate_count > MAX)
    {
        printf("Maximum number of candidates is %i\n", MAX);
        return 2;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i].name = argv[i + 1];
        candidates[i].votes = 0;
    }

    int voter_count = get_int("Number of voters: ");

    // Loop over all voters
    for (int i = 0; i < voter_count; i++)
    {
        string name = get_string("Vote: ");

        // Check for invalid vote
        if (!vote(name))
        {
            printf("Invalid vote.\n");
        }
    }

    // Display winner of election
    print_winner();
}

// Update vote totals given a new vote
bool vote(string name)
{
    for (int c = 0; c < candidate_count; c++)
    {
        if (strcmp(candidates[c].name, name) == 0)
        {
            candidates[c].votes++;
            return true;
        }
    }
    return false;
}

// Print the winner (or winners) of the election
void print_winner(void)
{
    //Sort candidates
    for (int c = 1; c < candidate_count; c++)
    {
        if (c != 0 && candidates[c].votes < candidates[c - 1].votes)
        {
            candidate curr = candidates[c];
            candidate prev = candidates[c - 1];
            candidates[c] = prev;
            candidates[c - 1] = curr;
            c -= 2;
        }
    }
    
    //Get the maximum number of votes
    int max_num_of_votes = candidates[candidate_count - 1].votes;

    //Print winner(s)
    for (int c = candidate_count - 1; c >= 0; c--)
    {
        if (candidates[c].votes == max_num_of_votes)
        {
            printf("%s\n", candidates[c].name);
        }
        else
        {
            break;
        }
    }
}