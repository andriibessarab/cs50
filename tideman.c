#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Max number of candidates
#define MAX 9

// preferences[i][j] is number of voters who prefer i over j
int preferences[MAX][MAX];

// locked[i][j] means i is locked in over j
bool locked[MAX][MAX];

// Each pair has a winner, loser
typedef struct
{
    int winner;
    int loser;
}
pair;

// Array of candidates
string candidates[MAX];
pair pairs[MAX * (MAX - 1) / 2];

int pair_count;
int candidate_count;

// Function prototypes
bool vote(int rank, string name, int ranks[]);
void record_preferences(int ranks[]);
void add_pairs(void);
void sort_pairs(void);
void lock_pairs(void);
bool is_cycle(int w, int l);
void print_winner(void);

int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: tideman [candidate ...]\n");
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
        candidates[i] = argv[i + 1];
    }

    // Clear graph of locked in pairs
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = 0; j < candidate_count; j++)
        {
            locked[i][j] = false;
        }
    }

    pair_count = 0;
    int voter_count = get_int("Number of voters: ");

    // Query for votes
    for (int i = 0; i < voter_count; i++)
    {
        // ranks[i] is voter's ith preference
        int ranks[candidate_count];

        // Query for each rank
        for (int j = 0; j < candidate_count; j++)
        {
            string name = get_string("Rank %i: ", j + 1);

            if (!vote(j, name, ranks))
            {
                printf("Invalid vote.\n");
                return 3;
            }
        }

        record_preferences(ranks);

        printf("\n");
    }

    // Clear graph of locked in pairs
    add_pairs();
    sort_pairs();
    lock_pairs();
    
    for (int j = 0; j < pair_count; j++)
    {
        printf("%i - %i\n", pairs[j].winner, pairs[j].loser);
    }
    
    for (int j = 0; j < candidate_count; j++)
    {
        printf("|");
        for (int i = 0; i < candidate_count; i++)
        {
            printf("%i|", locked[j][i]);
        }
        printf("\n");
    }
    
    print_winner();
    return 0;
}

// Update ranks given a new vote
bool vote(int rank, string name, int ranks[])
{
    for (int i = 0; i < candidate_count; i++)
    {
        if (strcmp(candidates[i], name) == 0)
        {
            ranks[rank] = i;
            return true;
        }
    }
    return false;
}

// Update preferences given one voter's ranks
void record_preferences(int ranks[])
{
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = i + 1; j < candidate_count; j++)
        {
            preferences [ranks[i]] [ranks[j]]++;
        }
    }
}

// Record pairs of candidates where one is preferred over the other
void add_pairs(void)
{
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = 0; j < candidate_count; j++)
        {
            if (j != i)
            {
                if (preferences [i] [j] > preferences [j] [i])
                {
                    pair_count++;
                    pairs[pair_count - 1].winner = i;
                    pairs[pair_count - 1].loser = j;
                }
            }
        }
    }
}

// Sort pairs in decreasing order by strength of victory
void sort_pairs(void)
{
    for (int i = 0; i < pair_count; i++)
    {
        if (i != 0
            && (preferences[pairs[i].winner][pairs[i].loser]
                - preferences[pairs[i].loser][pairs[i].winner]
                > preferences[pairs[i - 1].winner][pairs[i - 1].loser]
                - preferences[pairs[i - 1].loser][pairs[i - 1].winner]))
        {
            pair curr = pairs[i];
            pair prev = pairs[i - 1];
            pairs[i] = prev;
            pairs[i - 1] = curr;
            i -= 2;
        }
    }
}

// Lock pairs into the candidate graph in order, without creating cycles
void lock_pairs(void)
{
    for (int i = 0; i < pair_count; i++)
    {
        if (!(is_cycle(pairs[i].winner, pairs[i].loser)))
        {
            printf("-->%i - %i\n", pairs[i].winner, pairs[i].loser);
            locked [pairs[i].winner] [pairs[i].loser] = true;
        }
    }
    
}

//Check if cycle will be created after locking the next pair
bool is_cycle(int w, int l)
{
    printf("cyc\n");
    if (locked [l] [w])
    {
        return true;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        if (locked [i] [w])
        {
            return is_cycle(i, l);
        }
    }
    return false;
}

// Print the winner of the election
void print_winner(void)
{
    for (int j = 0; j < candidate_count; j++)
    {
        for (int i = 0; i < candidate_count; i++)
        {
            if (locked [i] [j])
            {
                break;
            }
            else if (i == candidate_count - 1)
            {
                printf("%s\n", candidates[j]);
                break;
            }
        }
    }
}