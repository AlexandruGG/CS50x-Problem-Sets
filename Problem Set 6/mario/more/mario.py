from cs50 import get_int

while True:
    height = get_int("Height: ")
    
    # Break only when the user provides a valid height
    if height > 0 and height < 9:
        break

for i in range(1, height + 1):
    # Number of hashes needed per line, per side
    hashes = "#" * i
    
    # Number of spaces needed before the left side hashes
    spaces = " " * (height - i)
    
    # Nicely formatted print statement
    print("{s}{h}  {h}".format(h=hashes, s=spaces))