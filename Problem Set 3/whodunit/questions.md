# Questions

## What's `stdint.h`?

A **header file** in the C standard library which provides a set of `typedefs` that specify exact-width integer types, together with the defined minimum and maximum allowable values for each type, using macros.

## What's the point of using `uint8_t`, `uint32_t`, `int32_t`, and `uint16_t` in a program?

They allow us to specify **exact sizes** in terms of bytes (or bits) that certain elements will occupy in memory.

## How many bytes is a `BYTE`, a `DWORD`, a `LONG`, and a `WORD`, respectively?

`BYTE` - 1 byte
`DWORD` - 4 bytes
`LONG` - 4 bytes
`WORD` - 2 bytes

## What (in ASCII, decimal, or hexadecimal) must the first two bytes of any BMP file be? Leading bytes used to identify file formats (with high probability) are generally called "magic numbers."

The first two bypes of a BMP file will be the characters `B` and `M` in ASCII.

## What's the difference between `bfSize` and `biSize`?

`bfSize` is the size, in bytes, of the entire bitmap file, whereas `biSize` is the size, in bytes, of the `BITMAPINFOHEADER` only.

## What does it mean if `biHeight` is negative?

It means the file is a top-down Device-Independent Bitmap (`DIB`) with the origin at the *upper left corner*.

## What field in `BITMAPINFOHEADER` specifies the BMP's color depth (i.e., bits per pixel)?

`biBitCount`

## Why might `fopen` return `NULL` in `copy.c`?

We might have failed to open the file because of, for example, specifying a non-existent file name.

## Why is the third argument to `fread` always `1` in our code?

Because we are reading 1 block at a time of a size specified in the second argument passed to the function.

## What value does `copy.c` assign to `padding` if `bi.biWidth` is `3`?

(4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4 = (4 - (3 * 3) % 4) % 4 = **3**

## What does `fseek` do?

It sets the file position indicator for the stream pointed to by the first parameter, `stream`, to a new position measured in bytes, obtained by adding the second parameter, `offset` to the position specified in the third parameter, `whence`. The offset can be relative to the start of the file, the current position, or the end of the file.

## What is `SEEK_CUR`?

It is one of third parameters that can be provided to the `fseek` function, signifying the current position indicator. The others are `SEEK_SET` - signifying the start of the file, and `SEEK_END` - signifying the end of the file.
