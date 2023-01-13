# --- Day 3: Rucksack Reorganization ---

You can find the original problem statement here: [https://adventofcode.com/2022/day/3](https://adventofcode.com/2022/day/3)

Part 1:

- The task is to find the item type that appears in both compartments of each rucksack, where each rucksack has two compartments, and all the items of a given type are meant to go into one compartment only.
- The input is a list of contents from several rucksacks, and the output is the sum of the priorities of the items that appear in both compartments of each rucksack.
- Every item type is identified by a single lowercase or uppercase letter, and priorities are assigned as such: lowercase items a-z have priorities 1-26, uppercase items A-Z have priorities 27-52.

Part 2:

- The task is to find the item type that is common between all three Elves in each group.
- The input is a list of contents from several rucksacks, but this time is grouped in set of three lines, each set corresponds to a single group of elves.
- The output is the item type that is common between all three elves in each group. Additionally, it is specified that the badge is the only item type carried by all three elves in each group, and at most two of the elves will be carrying any other item type.