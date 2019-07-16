from nltk.tokenize import sent_tokenize


# Compares two sets of lines from strings by splitting them based on \n characters and adding each one to a set
# The function then returns the intersection of the two sets - the elements they have in common
def lines(a, b):
    aLinesSet = set(a.splitlines())
    bLinesSet = set(b.splitlines())

    return aLinesSet & bLinesSet


# Compares two sets of sentences from strings by splitting them using the sent_tokenize function and adding each one to a set
# The function then returns the intersection of the two sets - the elements they have in common
def sentences(a, b):
    aSentencesSet = set(sent_tokenize(a))
    bSentencesSet = set(sent_tokenize(b))

    return aSentencesSet & bSentencesSet


# Compares two sets of substrings by first receiving them via the getSubstrings function and placing each one in a set
# The function then returns the intersection of the two sets - the elements they have in common
def substrings(a, b, n):
    aSubstringsSet = set(getSubstrings(a, n))
    bSubstringsSet = set(getSubstrings(b, n))

    return aSubstringsSet & bSubstringsSet


# Helper function which takes a string and returns all substrings of length n as a list
def getSubstrings(text, n):
    substringsList = []

    for i in range(len(text) - n + 1):
        substringsList.append(text[i:i + n])

    return substringsList