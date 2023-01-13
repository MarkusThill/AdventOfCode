# --- Day 13: Distress Signal ---

You can find the original problem statement here: [https://adventofcode.com/2022/day/13](https://adventofcode.com/2022/day/13)

Part 1:

The problem is asking to take a list of pairs of packets, where each packet is a list of integers or other lists, and determine which pairs are in the correct order. The correct order is determined by comparing the two packets element by element, where if both elements are integers, the lower integer should come first. If both elements are lists, compare the first element of each list, then the second element, and so on. If one value is an integer and the other is a list, the integer is converted to a list containing that integer, and then retry the comparison.
The problem needs to return the sum of the indices of the pairs that are in the correct order.

Part 2:

Part 2 of the problem is asking to organize all of the packets, including the list of received packets and the two additional divider packets: [[2]] and [[6]] into the correct order, by following the same rules used in part 1. After that, it needs to find the indices of the two divider packets and multiply them together to find the "decoder key" of the distress signal.
Return the decoder key.

