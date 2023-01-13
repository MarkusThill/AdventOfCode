# --- Day 14: Regolith Reservoir ---


You can find the original problem statement here: [https://adventofcode.com/2022/day/14](https://adventofcode.com/2022/day/14)

Part 1:

The problem is about simulating the falling of sand in a cave system. The cave system is described as a 2D vertical slice represented by a set of lines with x,y coordinates that forms the shape of the path, where x represents distance to the right and y represents distance down. Sand is produced one unit at a time, and it always falls down one step if possible. If the tile immediately below is blocked (by rock or sand), the unit of sand attempts to instead move diagonally one step down and to the left. If that tile is blocked, the unit of sand attempts to instead move diagonally one step down and to the right. Sand keeps moving as long as it is able to do so, at each step trying to move down, then down-left, then down-right. If all three possible destinations are blocked, the unit of sand comes to rest and no longer moves, at which point the next unit of sand is created back at the source. The task is to write a function that simulate the falling of sand using the description of the cave system and returns the number of units of sand that come to rest before sand starts flowing into the abyss below.

Part 2:

In Part 2 of the problem, it is specified that there is a floor at the bottom of the cave, that was not stated in Part 1. The y coordinate of the floor is equal to two plus the highest y coordinate of any point in the scan. The task is to simulate the falling of sand again as in Part 1 but this time the goal is to simulate it until a unit of sand comes to rest at point (500,0) blocking the source entirely and stopping the flow of sand into the cave, and return the number of units of sand that come to rest in the process.

