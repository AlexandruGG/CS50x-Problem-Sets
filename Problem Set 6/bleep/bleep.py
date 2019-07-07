from cs50 import get_string
from sys import argv


def main():
    # If the user doesn't provide exactly one argument, print usage and exit
    while len(argv) != 2:
        print("Usage: python bleep.py dictionary")
        exit(1)
        
    # Get the list of banned words from the dictionary provided    
    bannedWords = getBannedWords(argv[1])
    
    # Get the text message from the user
    text = get_string("What message would you like to censor?\n")
    
    # Get the list of words from the text input
    wordList = text.split()
    
    # Censor the message based on the list of banned words
    censoredMessage = censorMessage(wordList, bannedWords)
    print(censoredMessage)


# Function which opens the file passed in and reads each line, adding words 
# into a 'set' data structure
def getBannedWords(dictionary):
    words = set()
    file = open(dictionary, "r")
    
    for line in file:
        words.add(line.strip())
    
    file.close()
    return words
    
    
# Function which returns a censored message based on a word list and 
# a set of banned words passed in
def censorMessage(wordList, bannedWords):
    censoredList = []
    for word in wordList:
        if word.lower() in bannedWords:
            censoredList.append("*" * len(word))
        else:
            censoredList.append(word)
    return " ".join(censoredList)
    

if __name__ == "__main__":
    main()
