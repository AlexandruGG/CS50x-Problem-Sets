// Declares a dictionary's functionality

#ifndef DICTIONARY_H
#define DICTIONARY_H

#include <stdbool.h>

// Maximum length for a word
// (e.g., pneumonoultramicroscopicsilicovolcanoconiosis)
#define LENGTH 45

// Represents number of buckets in a hash table
// Based on https://www.usenix.org/legacy/publications/library/proceedings/als00/2000papers/papers/full_papers/lever/lever_html/index.html
// Equivalent to 512 MB RAM in buckets
#define N 131072

// Prototypes
bool load(const char *dictionary);
unsigned int size(void);
bool check(const char *word);
bool unload(void);

#endif // DICTIONARY_H
