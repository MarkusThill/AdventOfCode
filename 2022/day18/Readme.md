# --- Day 18: Boiling Boulders ---

You can find the original problem statement here: [https://adventofcode.com/2022/day/18](https://adventofcode.com/2022/day/18)

Part 1:

The problem is asking to calculate the surface area of a 3D shape represented by a set of 1x1x1 cubes on a 3D grid, given as their x, y, z coordinates. The surface area is calculated by counting the number of sides of each cube that are not immediately connected to another cube. The input to the problem is a scan of a lava droplet, represented as the coordinates of the cubes in the droplet, and the output should be the total surface area of the droplet.

Part 2:

In part 2 of the problem, the task is similar to part 1, but now the surface area calculated should only include the cube sides that could be reached by the water and steam, as the lava droplet tumbles into the pond. The steam will expand to reach as much as possible, completely displacing any air on the outside of the lava droplet but never expanding diagonally. The input to the problem is still a scan of the lava droplet, represented as the coordinates of the cubes in the droplet, and the output should be the exterior surface area of the droplet, not including the surface area of air pockets trapped inside the lava droplet.


## Solution sketch

The solution uses the numpy library to represent the 3D shape as a numpy array, where each element of the array is either 1 (meaning a cube is present at that position) or 0 (no cube at that position).

First, the input is read from a file, which contains the coordinates of the cubes as a list of strings in the format "x,y,z". These strings are parsed and converted into a list of integers, which are then used to populate the numpy array.

In part 1, the solution uses the np.diff() function to calculate the difference between adjacent elements along each axis of the numpy array. Specifically, the function is called three times, once for each axis, and the absolute value of the differences is taken in each case. The sum of these differences is then calculated and printed as the solution.

In part 2, the solution starts by finding the point that is outside of the droplet of lava, by using a modified BFS flood-fill algorithm to find all the points that are outside of the droplet and marking them as done. The number of done set is the number of points that are outside of the droplet. Then it uses the same method as in part1 to calculate the surface area of the droplet by calculating the difference between adjacent elements along each axis of the numpy array.

It then inverts the array such that the cubes that are inside the droplet are represented by 1's and the cubes that are outside the droplet are represented by 0's. The solution then finds the surface area of the droplet by summing the number of 1's on the edges of the array.

Finally, it prints the surface area of the droplet.