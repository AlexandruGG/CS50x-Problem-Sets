from cs50 import get_string
from sys import argv


def main():
    # If the user doesn't provide exactly one argument, print usage and exit
    while len(argv) != 2:
        print("Usage: python caesar.py k")
        exit(1)
    
    # Convert the key to an integer
    validKey = int(argv[1])
   
    # Get the plaintext from the user
    plaintext = get_string("plaintext: ")
    
    # Use a function to encrypt the plaintext
    ciphertext = encryptText(plaintext, validKey)
    
    # Return the encrypted text
    print("ciphertext: {c}".format(c=ciphertext))


# Function which encrypts a given text based on a key
def encryptText(plaintext, key):
    ciphertext = ''
    for i in range(len(plaintext)):
        # Check if the character is lowercase to use the right ASCII codes
        if (plaintext[i].islower()):
            ciphertext += chr(97 + (ord(plaintext[i]) + key - 97) % 26)
        # Check if the character is uppercase to use the right ASCII codes
        elif (plaintext[i].isupper()):
            ciphertext += chr(65 + (ord(plaintext[i]) + key - 65) % 26)
        # If the character is not alphabetical just add it to the ciphertext
        else:
            ciphertext += plaintext[i]
    return ciphertext
    
    
if __name__ == "__main__":
    main()