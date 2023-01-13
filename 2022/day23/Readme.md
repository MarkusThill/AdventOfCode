# --- Day 23: Unstable Diffusion ---

You can find the original problem statement here: [https://adventofcode.com/2022/day/23](https://adventofcode.com/2022/day/23)


Part 1:

The problem is about a group of elves that need to plant seedlings in a grove, but the grove is in a bad state and the plants rely on important nutrients from the ash. The ash is coming from a volcano and the ash should spread to the grove eventually. The elves need to spread out in the grove so that the plants are not too close together. The grove is represented by a grid of characters where '#' represents the elves and '.' represents empty ground. The elves need to move to new positions in the grove in a specific order, and if two or more elves propose to move to the same position, none of them move. The problem is to determine the final positions of the elves after a certain number of rounds, given the initial state of the grove as input and output the final positions of the elves in the same format as the input.

Part 2:

Part 2 of the problem is asking to continue the simulation of the process from Part 1 and determine the number of rounds where no elf moves. The input and output will be the same as Part 1, however, the output should be a single number that represents the number of the first round where no elf moves. The problem is to find the number of rounds needed for the elves to find the positions where they don't move.

## Rough Solution Sketch

The problem solution is a Python script that uses the Numpy library to simulate the movement of the elves in the grove. The script reads the initial state of the grove from a text file 'input23_1.txt' and converts it into a 2D array. It then uses a dictionary to store the positions of the elves, where the key is the index of the elf and the value is the position in the form of (x, y) coordinates.

The script uses two nested loops, an outer loop for the rounds and an inner loop for the elves. In the first half of each round, each elf considers the eight positions adjacent to themselves, and if no other elves are in one of those eight positions, the elf does not do anything during this round. Otherwise, the elf looks in each of four directions in the following order and proposes moving one step in the first valid direction. After each elf has had a chance to propose a move, the second half of the round can begin.

In the second half of each round, each elf moves to their proposed destination tile if they were the only elf to propose moving to that position. If two or more elves propose moving to the same position, none of them move. The script also keeps track of the number of rounds where no elf moves and the number of empty tiles in the grove after 10 rounds.

