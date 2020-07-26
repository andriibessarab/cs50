from cs50 import get_string

# Get text
text = get_string("Text: ")

# Declare variables
letters = 0
words = 1
sentences = 0

# Get num of letters, words, sentences
for i in range(len(text)):
    # Check if i is letter
    if text[i].isalpha():
        letters += 1

    # Check if i is space
    if text[i].isspace():
        words += 1

    # Check if i is . or ! or ?
    if text[i] == "." or text[i] == "!" or text[i] == "?":
        sentences += 1

# Calculate readability using Coleman-Liau index formula
index = 0.0588 * (letters * (100 / words)) - 0.296 * (sentences * (100 / words)) - 15.8

# Print results
if index < 1:
    print("Before Grade 1")
elif index > 16:
    print("Grade 16+")
else:
    print(f"Grade {round(index)}")
