# --- Day 12: Hill Climbing Algorithm ---

You can find the original problem statement here: [https://adventofcode.com/2022/day/12](https://adventofcode.com/2022/day/12)

Part 1:

The riddle describes a scenario in which the user is trying to reach a location with the best signal (E) while conserving energy. The user is given a heightmap of the surrounding area represented by a grid, with each square's elevation represented by a single lowercase letter. The user's current position (S) has elevation 'a' and the destination (E) has elevation 'z'. The user can move one square in any direction (up, down, left, or right) at a time, but the destination square's elevation cannot be more than one higher than the current square's elevation. The task is to find the fewest steps required to reach the location with the best signal.

Part 2:

In part two of the riddle, the task is to find the shortest path from any square with elevation a to the location with the best signal (E) while maximizing exercise. The trail should start as low as possible and take the fewest steps to reach its goal. The user needs to find the fewest steps required to move from any square with elevation 'a' to the location that should get the best signal (E)