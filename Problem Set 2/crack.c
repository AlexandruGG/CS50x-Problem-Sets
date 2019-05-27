#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <crypt.h>

int main(int argc, string argv[])
{
    int crackPassword(string hash, char salt[3], string dictionary, int dictionaryLength);
    
    // Exit the program if the user did not provide exactly 1 argument with the command.
    if (argc != 2)
    {
        printf("Usage: ./crack hash\n");
        return 1;
    }
    
    // Dictionary of characters based on the most used letters in the English language;
    // Source: https://en.wikipedia.org/wiki/Letter_frequency.
    string dictionary = "etaoinshrdlcumwfgypbvkjxqzETAOINSHRDLCUMWFGYPBVKJXQZ";
    
    // Adding '\0 at the beginning of the dictionary will help test shorter password first'.
    string modifiedDictionary = "\0etaoinshrdlcumwfgypbvkjxqzETAOINSHRDLCUMWFGYPBVKJXQZ";

    int dictionaryLength = strlen(dictionary) + 1;
    string hash = argv[1];
    
    // Initialise salt based on the first 2 characters of the hash.
    char salt[3] = {hash[0], hash[1], '\0'};

    int cracked = crackPassword(hash, salt, modifiedDictionary, dictionaryLength);
    
    if (cracked == 1)
    {
        printf("Password uncrackable! Might be more than 5 characters long.\n");
        return 1;
    }
    else
    {
        return 0; 
    }
}

// Function which cracks a DES-hashed password of maximum 5 characters in length by brute force
// by iterating over the dictionary characters. One loop is used for each of the characters in the password,
// starting from the last one.
int crackPassword(string hash, char salt[3], string dictionary, int dictionaryLength)
{
    char testPassword[6];
    
    for (int i = 0; i < dictionaryLength; i++)
    {
        for (int j = 0; j < dictionaryLength; j++)
        {
            for (int k = 0; k < dictionaryLength; k++)
            {
                for (int l = 0; l < dictionaryLength; l++)
                {
                    for (int m = 1; m < dictionaryLength; m++)
                    {
                        testPassword[0] = dictionary[m];
                        testPassword[1] = dictionary[l];
                        testPassword[2] = dictionary[k];
                        testPassword[3] = dictionary[j];
                        testPassword[4] = dictionary[i];
                        
                        // The strcmp function will return 0 if the two strings are equal.
                        if (strcmp(crypt(testPassword, salt), hash) == 0)
                        {
                            printf("Cracked Password: %s\n", testPassword);
                            return 0;
                        }
                        
                        // Printing each tested combination multiple times just for visual feedback for the user.
                        // I think it looks cool :).
                        printf("%s  %s  %s  %s  %s  %s  %s  %s  %s  %s\n", testPassword, testPassword, testPassword, testPassword, testPassword, 
                               testPassword, testPassword, testPassword, testPassword, testPassword);
                    }
                }
            }
        }
    }
    
    // If the function reaches this point it means the password could not be cracked.
    // This might be because the hash provided is for a password > 5 characters in length.
    return 1;
}
