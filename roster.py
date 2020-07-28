from cs50 import SQL
from sys import argv

# Validate argv
if len(argv) != 2:
    print("Usage: python roaster.py house")

# Print students of specified house
db = SQL("sqlite:///students.db")
info = db.execute("SELECT first, middle, last, birth FROM students WHERE house = ? ORDER BY last, first", argv[1])
for i in info:
    print(f"{i['first']} {i['middle'] + ' ' if i['middle'] != None else ''}{i['last']}, born {i['birth']}")
