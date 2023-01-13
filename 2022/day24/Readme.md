# --- Day 24: Blizzard Basin ---

You can find the original problem statement here: [https://adventofcode.com/2022/day/24](https://adventofcode.com/2022/day/24)


Part 1:
The problem describes a valley that is represented by a map, where the walls are represented by "#" and the ground is represented by ".". Some of the ground positions contain blizzards represented by an arrow (^, v, <, >) indicating their direction of motion. The goal is to reach the only non-wall position in the bottom row while avoiding the blizzards. Each minute, the blizzards move one position in the direction they are pointing, and a new blizzard forms on the opposite side of the valley if a blizzard reaches the wall. The person starts in the only non-wall position in the top row and can move up, down, left, or right, or wait in place each minute, simultaneously with the blizzards. The task is to find the minimum number of minutes required to reach the goal.

Part 2:

In part 2 of the problem, The task is to find the fewest number of minutes required to reach the goal, go back to the start, and then reach the goal again. The initial conditions are the same as in part 1, which means the starting point, the map of the valley and the blizzards, and the movement rules are the same. However, this time the goal is to make two trips, one from the start to the goal, then back to the start, and then back to the goal. Similar to part 1, the task is to find the minimum number of minutes required to complete the two trips while avoiding the blizzards.

## Solution Sketch



This solution uses a breadth-first search (BFS) algorithm to find the minimum number of minutes required to reach the goal in both parts of the problem. The solution is implemented in Python and makes use of the numpy and collections libraries.

The input is read from a text file, which is then parsed to create a 2D array that represents the map of the valley and the blizzards. The initial position of the blizzards is stored in a dictionary, and the board state for t=0 is generated. The solution pre-generates all board positions for t>0 and stores them in a dictionary.

The BFS algorithm starts by adding the initial state to a queue, where the state is represented by a tuple containing the time, the row and column of the current position, a flag indicating if the goal has been reached, and a flag indicating if the start has been reached. The algorithm then repeatedly pops the first state from the queue and checks if it has been visited before.

If the state has not been visited before, the algorithm checks if the current position is the goal and updates the solution if it is. If the goal has been reached, the algorithm checks if the start has also been reached, and if it has, the algorithm terminates. If the goal has not been reached, the algorithm generates the next possible states by moving to the adjacent cells, and adds them to the queue.

The algorithm continues this process until the goal has been reached and the start has been reached again in part 2. The final solution is the number of minutes required to reach the goal.