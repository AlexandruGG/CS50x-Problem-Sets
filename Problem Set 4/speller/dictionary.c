// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Represents a hash table
node *hashtable[N];

// Variable which will be used in the size function to return the number of words loaded
int wordCount = 0;

// Hash function based on the well-known djb2
// Source: http://www.cse.yorku.ca/~oz/hash.html
unsigned int hash(const char *word)
{
    unsigned long hash = 5381;
    int c;

    while ((c = *word++))
    {
        hash = ((hash << 5) + hash) + c;
    }
    
    return hash % N;
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    // Initialize hash table
    for (int i = 0; i < N; i++)
    {
        hashtable[i] = NULL;
    }

    // Open dictionary
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        unload();
        return false;
    }

    // Buffer for a word
    char word[LENGTH + 1];

    // Insert words into hash table
    while (fscanf(file, "%s", word) != EOF)
    {
        // Initialize new node
        node *newNode = malloc(sizeof(node));
        
        if (!newNode)
        {
            fclose(file);
            return false;
        }
        
        // Add the newly read word to the new node
        strcpy(newNode->word, word);
        newNode->next = NULL;

        // Get the dictionary index for the word via the hash function
        int i = hash(word);
        
        // If don't already have a linked list created at index i,
        // initialize it with the new node. Otherwise, add the new node
        // to the existing list
        if (!hashtable[i])
        {
            hashtable[i] = newNode;
        }
        else
        {
            newNode->next = hashtable[i];
            hashtable[i] = newNode;
        }
        
        wordCount++;
    }

    // Close dictionary
    fclose(file);

    // Indicate success
    return true;
}

// Returns number of words in dictionary (will return 0 if none were loaded)
unsigned int size(void)
{
    return wordCount;
}

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    // Copy word to another variable so it can be changed to lowercase
    char lowerWord[strlen(word) + 1];
    strcpy(lowerWord, word);
    
    // Convert copied word to lowercase
    for (int i = 0; lowerWord[i]; i++)
    {
        lowerWord[i] = tolower(lowerWord[i]);
    }
    
    // Get the dictionary bucket for the word via the hash function
    int bucket = hash(lowerWord);
    
    // If there is no bucket, the word is not in the dictionary
    if (!hashtable[bucket])
    {
        return false;
    }
    
    node *cursor = hashtable[bucket];
    
    // Check each node of the list for the word and return true if found
    while (cursor != NULL)
    {
        if (strcasecmp(lowerWord, cursor->word) == 0)
        {
            return true;
        }
        cursor = cursor->next;
    }

    // If we reached this point, the word is not in the dictionary
    return false;
}

// Unloads dictionary from memory, returning true upon finishing
bool unload(void)
{
    // Run through each bucket in the dictionary
    for (int i = 0; i < N; i++)
    {
        node *cursor = hashtable[i];
        
        // Run through each node in a given bucket and free it
        while (cursor != NULL)
        {
            node *temp = cursor;
            cursor = cursor->next;
            free(temp);
        }
    }
    
    return true;
}
