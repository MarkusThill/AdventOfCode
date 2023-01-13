<img src="https://github.com/MarkusThill/AdventOfCode/blob/890e8af0ad05a019a51cb65511a411d7e5a9953d/2022/day19/robots.png" width="500" height="500">

# --- Day 19: Not Enough Minerals ---

You can find the original problem statement here: [https://adventofcode.com/2022/day/19](https://adventofcode.com/2022/day/19)

Part 1:

The problem is about creating robots to open geodes in 24 minutes. The robots need to collect obsidian, clay, and ore. The obsidian-collecting robots need to be waterproof and made from clay, the clay-collecting robots need to be special-purpose and made from ore, and the ore-collecting robots need to have big drills. The problem requires the use of a robot factory with many blueprints (input) to determine which blueprint would maximize the number of opened geodes in 24 minutes. The solution to the problem is to calculate the quality level of each blueprint by multiplying the blueprint's ID number by the largest number of geodes that can be opened in 24 minutes using that blueprint, and then adding up the quality level of all blueprints to get the final answer.

Part 2:

In part 2 of the problem, the time available to open geodes has increased to 32 minutes and only the first 3 blueprints in the list are available. The task is to determine the largest number of geodes that can be opened using each of the first three blueprints. Then, multiply these three values together to get the final answer. Quality levels are no longer a concern in this part of the problem.

## Solution Sketch

The solution to the problem is implemented in C++ and makes use of several C++ features such as templates, constexpr, tuple, unordered_map, and index_sequence.

In part 1 of the problem, the solution uses a for loop to iterate over all the blueprints available in the input. The solution uses a tuple to store the resources (ore, clay, obsidian, geode, ore robot, clay robot, obsidian robot, geode robot, time left) required for each blueprint and a vector to store the quality level of each blueprint. The solution also uses an unordered_map to store the maximum number of geodes that can be opened using each blueprint.

The function takes all the resources and the time left as input and returns the maximum number of geodes that can be opened using the blueprint. The function iterates over all the blueprints, updates the resources and time left, and calculates the quality level of each blueprint by multiplying the blueprint's ID number with the number of geodes that can be opened using that blueprint. The final answer is obtained by adding up the quality level of all the blueprints.

In part 2, the solution is similar to part 1 but instead of calculating the quality level of each blueprint, the solution calculates the maximum number of geodes that can be opened using the first 3 blueprints and then multiplies these 3 numbers together to get the final answer.

Both parts of the solution uses an unordered_map with a custom hash function and key comparator to store the number of geodes that can be opened by each blueprint. The solution also uses a tuple to store the resources and time left. The solution also uses a helper function 'vectorToTupleHelper' to convert the vector to tuple. The function 'generateRandVector' is used to generate random numbers for an unordered_map.

