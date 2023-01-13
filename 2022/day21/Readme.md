#--- Day 21: Monkey Math ---

You can find the original problem statement here: [https://adventofcode.com/2022/day/21](https://adventofcode.com/2022/day/21)


Part 1:

This problem is about a group of monkeys, each of which has a specific task: either to yell a number or to yell the result of a math operation. The math operation monkeys have to wait for two other monkeys to yell their numbers before they can yell their own number. The task is to determine the number that the monkey named 'root' will yell. Each line of input contains the name of a monkey, a colon, and then the task of that monkey. Tasks can include simply yelling a number, adding two numbers, subtracting two numbers, multiplying two numbers or dividing two numbers. The goal is to use this information to find the number that 'root' monkey will yell.

Part 2:

In Part 2 of the problem, you misunderstood the task assigned to the monkey named 'root', which is now supposed to check if two numbers match instead of doing a math operation. Additionally, the task assigned to the "humn" is actually for you to figure out the number you need to yell to make the root's equality check pass. The goal is to find the number that you need to yell to make the root's equality check pass. The number that appears after "humn:" is now irrelevant. You need to find the number that causes root to get the same number from both of its monkeys.

## Solution Sketch

This problem is solved in Python using the libraries numpy, networkx, and time. The solve() function takes three parameters: a directed graph (G) that contains the information about the monkeys and their tasks, an integer (part) that indicates whether the problem is part 1 or part 2, and an optional parameter (repl) that is used in part 2 of the problem.

For part 1 of the problem, the function starts at the root monkey and traverses the graph using depth-first search. When it encounters a monkey that is assigned a math operation, it checks if the values of the two operands are available. If they are, it performs the operation and saves the result. If not, it goes to the monkey that is assigned the missing operand. The function continues traversing the graph in this way until it reaches a monkey that is assigned a number. At this point, it goes back up the tree and continues traversing until it reaches the root monkey. At this point, it returns the value of the root monkey, which is the answer to the problem.

For part 2 of the problem, the function starts at the root monkey and traverses the graph in the same way as before. However, instead of performing the operation, it keeps track of the two operands and returns them. Then, it uses a bisection method to find the value that the "humn" monkey should yell to make the root monkey's equality check pass.

It starts by setting an interval for the value that "humn" monkey should yell, and then it checks the difference between the two operands for different values of this interval. It keeps reducing the interval and checking the difference until the error is less than a certain threshold. The value of "humn" monkey that makes the difference zero is the solution to the problem.