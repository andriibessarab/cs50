import csv
from sys import argv, exit
from cs50 import SQL

# Validate argv
if (len(argv) != 2 or not argv[1].endswith('.csv')):
    print("Usage: python import.py characters.csv")
    exit()

try:

    # Open csv
    with open(argv[1]) as f:
        # Read csv and open db
        csv = csv.DictReader(f)
        db = SQL("sqlite:///students.db")

        # Add students to db
        for i in csv:
            name = i["name"].split(" ")
            if len(name) == 3:
                db.execute("INSERT INTO students (first, middle, last, house, birth) VALUES (?, ?, ?, ?, ?)",
                           name[0], name[1], name[-1], i["house"], i["birth"])
            else:
                db.execute("INSERT INTO students (first, middle, last, house, birth) VALUES (?, ?, ?, ?, ?)",
                           name[0], None, name[-1], i["house"], i["birth"])

except FileNotFoundError:

    print(f"Could not open {argv[1]}")
    exit()

exit()
