#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    int blockSize = 512;
    
    // ensure proper usage
    if (argc != 2)
    {
        fprintf(stderr, "Usage: ./recover image\n");
        return 1;
    }
    
    // open memory card file
    FILE *memfile = fopen(argv[1], "r");
    if (memfile == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", argv[1]);
        return 2;
    }
    
    // prepare variables for reading new file and writing JPEGs
    unsigned char *buffer = malloc(blockSize);
    FILE *validJPEG = NULL;
    int imageNumber = 0;
    
    // read the memory card while we haven't reached EOF
    while (fread(buffer, blockSize, 1, memfile))
    {
        // if we found the start of a JPEG
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            // close previous JPEG file if it exists
            if (imageNumber > 0)
            {
                fclose(validJPEG);
            }
            
            // prepare new JPEG file
            char filename[8];
            sprintf(filename, "%03i.jpg", imageNumber);
            
            // write to new JPEG file
            validJPEG = fopen(filename, "w");
            
            imageNumber++;
        }
        
        // if we already created a new image, write bytes to it
        if (imageNumber > 0)
        {
            fwrite(buffer, blockSize, 1, validJPEG);
        }
    }
    
    // free the buffer pointer
    free(buffer);
    
    // close the memory card file
    fclose(memfile);
    
    // close the last JPEG file
    fclose(validJPEG);

    return 0;
}
