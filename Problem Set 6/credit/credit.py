from cs50 import get_int


def main():
    cardNumber = get_int("Number: ")
    
    cardIsValid = isValid(cardNumber)
    card = cardType(cardNumber)
    
    if cardIsValid:
        print(card)
    else:
        print("INVALID")


# Function which checks the card type based on the first 1 or two digits
def cardType(cardNumber: int) -> str:
    visa = [4]
    amex = [34, 37]
    masterCard = [51, 52, 53, 54, 55]
    
    while cardNumber >= 100:
        cardNumber //= 10
    
    if cardNumber // 10 in visa:
        return "VISA"
    elif cardNumber in amex:
        return "AMEX"
    elif cardNumber in masterCard:
        return "MASTERCARD"
    else:
        return "INVALID"


# Function which checks if the card is valid based on Luhn's algorithm
def isValid(cardNumber: int) -> bool:
    finalSum = 0
    sumProductDigits = 0
    digitList = []
    digitListCounter = 0
    
    # Using a while loop to add all card number digits in a list, in reverse order
    while True:
        if cardNumber == 0:
            break
        digitList.append(cardNumber % 10)
        cardNumber //= 10
        digitListCounter += 1

    # If the number of digits is not 13, 14, or 15 -> the card is invalid
    if digitListCounter not in [13, 14, 15, 16]:
        return False
    
    # Looping over each digit in the list to make the necessary calculations
    for index, digit in enumerate(digitList):
        if index % 2 != 0:
            multipliedDigit = digit * 2
            if multipliedDigit < 10:
                sumProductDigits += multipliedDigit
            else:
                sumProductDigits += multipliedDigit // 10 + multipliedDigit % 10
        else:
            finalSum += digit
            
    finalSum += sumProductDigits
    
    if finalSum % 10 == 0:
        return True
    else:
        return False


if __name__ == "__main__":
    main()