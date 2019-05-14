#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int height;
    
    do
    {
        height = get_int("Height: ");
    }
    while (height < 1 || height > 8);
    
    for (int i = 1; i <= height; i++)
    {
        for (int j = height; j >= 1; j--)
        {
            if (j > i)
            {
                printf(" ");
            }
            else
            {
                printf("#");
            }
        }
        printf("  ");
        for (int j = 1; j <= height; j++)
        {
            if (j <= i)
            {
                printf("#");
            }
        }
        printf("\n");
    }
}