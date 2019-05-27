#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>

int main(int argc, string argv[])
{
    bool isValidKey(int argc, string key);
    string encryptText(string plaintext, int key);
    
    // Quit the program if exactly 1 argument was not provided
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    } 
        
    if (!isValidKey(argc, argv[1]))
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
    
    // Convert the key to an integer
    int validKey = atoi(argv[1]);
    
    string plaintext = get_string("plaintext: ");
    string ciphertext = encryptText(plaintext, validKey);
    
    printf("ciphertext: %s\n", ciphertext);
    
    return 0; 
}

// Checks whether the key provided in the command is valid
bool isValidKey(int argc, string key) 
{
    for (int i = 0; i < strlen(key); i++)
    {
        if (!isdigit(key[i]))
        {
            return false;
        }
    }
    
    return true;
}

// Encrypts the plaintext provided by the user
string encryptText(string plaintext, int key)
{
    for (int i = 0; i < strlen(plaintext); i++)
    {       
        if (islower(plaintext[i]))
        {
            plaintext[i] = 97 + (plaintext[i] + key - 97) % 26;
        } 
        else if (isupper(plaintext[i]))
        {
            plaintext[i] = 65 + (plaintext[i] + key - 65) % 26;
        }
    }
    
    return plaintext;
}
