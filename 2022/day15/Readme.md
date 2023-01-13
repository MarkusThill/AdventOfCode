# --- Day 15: Beacon Exclusion Zone ---

You can find the original problem statement here: [https://adventofcode.com/2022/day/15](https://adventofcode.com/2022/day/15)


Part 1:

You have a set of sensors and beacons that exist at integer coordinates. Each sensor can determine the position of the closest beacon to it using Manhattan distance. You are given a set of sensor and beacon positions as input. Your task is to find the number of positions on a specific row (y=2000000) where a beacon cannot possibly be located. You have to use the information provided by the sensors and their closest beacons to make this determination.

Part 2:

The distress signal is coming from a nearby beacon, but it is not detected by any sensor. The distress beacon must have x and y coordinates each no lower than 0 and no larger than 4000000. To find the distress beacon, you need to determine its tuning frequency by multiplying its x coordinate by 4000000 and then adding its y coordinate. In the given example, the search area is reduced and the x and y coordinates can each be at most 20. Your task is to find the only possible position for the distress beacon and its tuning frequency.

