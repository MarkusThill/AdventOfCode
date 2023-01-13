# --- Day 20: Grove Positioning System ---

You can find the original problem statement here: [https://adventofcode.com/2022/day/20](https://adventofcode.com/2022/day/20)

Part 1:

The challenge is to decrypt an encrypted file which is a list of numbers. The main operation involved in decrypting the file is called mixing. To mix the file, move each number forward or backward in the file a number of positions equal to the value of the number being moved. The list is circular, so moving a number off one end of the list wraps back around to the other end as if the ends were connected. After mixing the file, we need to find the sum of the 1000th, 2000th and 3000th numbers after the value 0, wrapping around the list as necessary.

Part 2:

In Part 2 of the problem, the decryption routine is slightly different than before. First, we need to multiply each number by the decryption key, 811589153, before applying the mixing operation. Then, we need to mix the list of numbers ten times, instead of just once. After mixing the list ten times, we need to find the sum of the 1000th, 2000th and 3000th numbers after the value 0, wrapping around the list as necessary.

## Solution Sketch

The solution is written in Python and it consists of two functions, day20_1() and day20_2(), which correspond to the first and second parts of the problem respectively.

day20_1() function:

1. The function opens a file called 'input20_1.txt' and reads its contents into a list called 'lines'.
2. The list is then cleaned up by stripping each line of any whitespace.
3. Then, a new list called 'mylist' is created which contains the values from 'lines' as integers, along with the original position of each value in the file 'input20_1.txt'.
4. In a for loop, for each value in 'mylist', it finds the index of the value in 'mylist', removes it from the list, calculates its new position by adding its value to its current index and taking the modulus of the sum with the length of 'mylist', and then inserting it back into 'mylist' at the new position.
5. After the loop, the 'mylist' is modified to only contain the values and not their original positions.
6. The index of 0 in 'mylist' is found and used to calculate the sum of the 1000th, 2000th and 3000th values after 0.
7. The sum is printed as the solution for part 1 of the problem.

day20_2() function:

1. The function is similar to day20_1() function but with some additional steps before the loop:
2. Each value in the list is multiplied by 811589153.
3. The for loop runs 10 times and the rest of the steps are same as in day20_1 function.
4. The sum is printed as the solution for part 2 of the problem.

