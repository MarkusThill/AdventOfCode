# --- Day 25: Full of Hot Air ---

You can find the original problem statement here: [https://adventofcode.com/2022/day/25](https://adventofcode.com/2022/day/25)

You are given a list of fuel requirements for hot air balloons in a special number format called "SNAFU" (Special Numeral-Analogue Fuel Units). SNAFU numbers are similar to regular numbers, but use powers of five instead of powers of ten. Starting from the right, there is a ones place, a fives place, a twenty-fives place, a one-hundred-and-twenty-fives place, and so on. Instead of using the digits four through zero, the digits are 2, 1, 0, minus (-), and double-minus (=). The minus sign is worth -1 and double-minus is worth -2. Your task is to decipher the fuel requirements in the SNAFU format and find the total amount of fuel needed.

## Solution Sketch

The solution reads a file named 'input25_1.txt' which contains the fuel requirements in SNAFU format. Each line of the file is a separate fuel requirement. It removes the newline characters from the lines and converts them into lists of characters.

The function 'to_decimal' takes a list of characters representing a SNAFU number and converts it into a decimal number. It initializes a variable 'p' to 1, which represents the current power of 5. It iterates through the characters in reverse order, and for each character, it does the following:

If the character is '0', it adds 0 to the variable 'num'.
If the character is '1', it adds 'p' to the variable 'num'.
If the character is '2', it adds 2*'p' to the variable 'num'.
If the character is '-', it subtracts 'p' from the variable 'num'.
If the character is '=', it subtracts 2*'p' from the variable 'num'.
It multiplies 'p' by 5.
At the end, it returns the variable 'num' as the decimal representation of the SNAFU number.

The function 'to_decimal2' is similar to 'to_decimal', but it takes a list of integers instead of a list of characters, and it does not check for '=' and '-' characters, as the input is already converted to integers.

The 'day25_1' function uses the 'to_decimal' function to convert all the fuel requirements in the input file to decimal numbers and adds them together to find the total amount of fuel needed. Then it uses 'to_decimal2' function to convert the total fuel needed back to SNAFU format. It finds the closest representation of each digit by iterating through the range of -2 to 2 and keeps the representation that has the smallest difference to the desired decimal number.