<img src="https://github.com/MarkusThill/AdventOfCode/blob/main/2023/day24/img.png" width="500" height="500">

# --- Day 24: Never Tell Me The Odds ---

You can find the original problem statement here: [https://adventofcode.com/2023/day/24](https://adventofcode.com/2023/day/24)


Part 1:

The problem involves hailstones moving through the air with given initial positions and velocities. The task is to determine how many of these hailstones' paths will intersect within a specified test area, considering only the X and Y axes. The intersections are checked by comparing pairs of hailstones' future paths. The example provides a test area with boundaries and demonstrates the process of identifying intersecting paths. The puzzle answer for the given data is not mentioned here.

Part 2:

After realizing that hailstones won't naturally collide, the goal is to throw a rock in a way that it collides with every hailstone. The rock can be thrown with a specified position and velocity. The task is to find the exact position and velocity of the rock at time 0 to achieve perfect collisions with all hailstones. The sum of the X, Y, and Z coordinates of the rock's initial position is required as the answer. The example illustrates how to determine the collision times and positions for each hailstone. The solution for the given data, which is not mentioned here, is the sum of the X, Y, and Z coordinates of the rock's initial position.


## Solution Sketch

In Part One, the code iterates through pairs of hailstones and checks if their linear trajectories intersect within a specified test area on the X and Y axes. The intersection is determined by solving a system of linear equations representing the paths of the two hailstones. The resulting count of intersections within the test area is then printed as the solution.

For Part Two, the code utilizes the Z3 solver to find the exact position and velocity for a rock to simultaneously collide with every hailstone. It defines variables for the rock's starting position (x, y, z) and velocity (v_x, v_y, v_z). Equations representing the positions of the rock at a given time, relative to each hailstone, are set up. The Z3 solver is then used to check for a solution, and the sum of the X, Y, and Z coordinates of the rock's initial position is printed as the solution.

