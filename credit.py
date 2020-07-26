from cs50 import get_int


# Main function
def main():
    # Get card number
    card = get_int("Number: ")

    # Check if card is valid
    if (checksum(card)):
        # Check if card is AMEX
        if len(str(card)) == 15 and (int(str(card)[:2]) == 34 or int(str(card)[:2]) == 37):
            print("AMEX")

        # Check if card is MASTERCARD
        elif len(str(card)) == 16 and (int(str(card)[:2]) >= 51 and int(str(card)[:2]) <= 55):
            print("MASTERCARD")

        # Check if card is VISA
        elif (len(str(card)) == 13 or len(str(card)) == 16) and int(str(card)[0]) % 10 == 4:
            print("VISA")

        else:
            print("INVALID")
    else:
        print("INVALID")


# Checksum function
def checksum(card):
    total = 0

    # Count total
    while (card > 0):
        total += card % 10
        card //= 10
        if (card == 0):
            break
        n = (card % 10) * 2
        total += (n % 10) + (n // 10)
        card //= 10

    # Check if total % 10 equals 0
    if (total % 10 == 0):
        return True
    return False


# Call main function
if __name__ == "__main__":
    main()
