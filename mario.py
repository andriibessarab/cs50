from cs50 import get_int


# Main function
def main():
    # Get height
    height = get_height()

    # Print pyramid
    print_pyramid(height)


# Get height function
def get_height():
    # Get height
    height = get_int("Height: ")

    # Check if height is between 1 and 8
    if height < 1 or height > 8:
        return get_height()

    # Return height
    return height


# Print pyramid function
def print_pyramid(h, l=None):
    # If length is None set it equal to height
    if l == None:
        l = h

    # Stop if length is 0
    if l == 0:
        return

    # Print shorter row first
    print_pyramid(h, l - 1)

    # Print spaces
    print(" " * int(h - l), end="")

    # Print bricks(left side)
    print("#" * int(l), end="")
    
    # Print two spaces
    print("  ", end="")
    
    # Print bricks(right side)
    print("#" * int(l), end="")

    # Start a new line
    print()


# Call main function
if __name__ == "__main__":
    main()
