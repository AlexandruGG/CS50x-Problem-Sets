#include <stdio.h>
#include <cs50.h>

int main(void)
{
    long cardNumber = get_long("Number: ");
    string cardType(long cardNumber);
    bool isValid(long cardNumber);
    
    bool cardIsValid = isValid(cardNumber);
    string card = cardType(cardNumber);

    if (cardIsValid)
    {
        printf("%s", card);
    } 
    else 
    {
        printf("INVALID\n");
    }
}

string cardType(long cardNumber)
{  
    int visa[] = {4};
    int amex[] = {34, 37};
    int masterCard[] = {51, 52, 53, 54, 55};
    
    while (cardNumber >= 100)
    {
        cardNumber /= 10;
    }

    if (cardNumber / 10 == visa[0])
    {
        return "VISA\n";
    }
    else if (cardNumber == amex[0] || cardNumber == amex[1])
    {
        return "AMEX\n";
    }
    else
    {
        for (int i = 0; i < 5; i++)
        {
            if (cardNumber == masterCard[i])
            {
                return "MASTERCARD\n";
            }
        }     
        return "INVALID\n";
    }  
}

bool isValid(long cardNumber)
{
    long digit[20] = {};
    int multipliedDigit[20] = {};
    int digitArrayCounter = 0;
    int productArrayCounter = 0;
    int sumProductDigits = 0;
    int finalSum = 0;

    do 
    {
        digit[digitArrayCounter] = cardNumber % 10;
        cardNumber /= 10;
        digitArrayCounter++;
    }
    while (cardNumber != 0);
    
    if (digitArrayCounter < 13 || digitArrayCounter > 16)
    {
        return false;
    }
    
    for (int i = 0; i < digitArrayCounter; i++)
    {
        if (i % 2 != 0)
        {
            multipliedDigit[productArrayCounter] = digit[i] * 2;

            if (multipliedDigit[productArrayCounter] < 10)
            {
                sumProductDigits += multipliedDigit[productArrayCounter];
            }
            else
            {
                sumProductDigits += multipliedDigit[productArrayCounter] / 10 + multipliedDigit[productArrayCounter] % 10;
            }
            
            productArrayCounter++;
        }
        else
        {
            finalSum += digit[i];    
        }
    }
        
    finalSum += sumProductDigits;
    
    if (finalSum % 10 == 0)
    {
        return true;
    }
    else
    {
        return false;
    }
}
