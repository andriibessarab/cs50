import csv
from sys import argv, exit

# Validate database and sequence
if (len(argv) != 3 or not argv[1].endswith('.csv') or not argv[2].endswith('.txt')):
    print("Usage: python dna.py data.csv sequence.txt")
    exit()

# Declare vars
users = {}
STRs = {}
sequence = []

# Open database
try:

    with open(argv[1]) as f:
        db = csv.DictReader(f)

        # Make dict with STRs
        for i in db.fieldnames[1:]:
            STRs[i] = 0

        # Make dict with users
        for i in db:
            users[i["name"]] = {}

            for s in STRs:
                users[i["name"]][s] = int(i[s])

# Raise error if could not open database
except FileNotFoundError:

    print(f"Could not open {argv[1]}")
    exit()

# Open sequence
try:

    with open(argv[2]) as f:
        sq = (f.read())

        # Convert sequence to list
        for i in sq:
            if i != "\n":
                sequence.append(i)

# Raise error if could not open sequence
except FileNotFoundError:

    print(f"Could not open {argv[2]}")
    exit()

# Insert sequence data into STRs dict
for i in range(len(sequence)):

    if i != "\n":

        for s in STRs:
            c = 0

            if len(sequence) - i < len(s):
                break

            while("".join(sequence[i:i + len(s)]) == s):

                c += 1
                i += len(s)

            if c > STRs[s]:
                STRs[s] = c

# Check if sequence belongs to anyone in database
for i in users:
    c = 0

    for s in STRs:
        if STRs[s] == users[i][s]:
            c += 1

    if c == len(STRs):
        print(i)
        exit()

print("No match")
exit()
