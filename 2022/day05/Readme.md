# --- Day 5: Supply Stacks ---

You can find the original problem statement here: [https://adventofcode.com/2022/day/5](https://adventofcode.com/2022/day/5)

In Part 1 of this problem, there are three stacks of crates, and the task is to determine the order of the top crates after a series of carefully-planned steps to rearrange them. In each step, a quantity of crates is moved from one stack to a different stack. The crates are moved one at a time, so their order relative to each other does not change. The goal is to determine the top crate of each stack after the rearrangement procedure is complete. In the example given, the top crates are C in stack 1, M in stack 2, and Z in stack 3.

In Part 2, the problem is the same as Part 1, but the CrateMover 9001 is used which has the ability to move multiple crates at once, and in the order they are in the stack. So, moving three crates from stack 1 to stack 3 means that those three crates stay in the same order, resulting in a new configuration, for example in the sample in the example the three crates D, N and C will remain in the same order after the movement.