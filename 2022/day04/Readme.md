# --- Day 4: Camp Cleanup ---
You can find the original problem statement here: [https://adventofcode.com/2022/day/4](https://adventofcode.com/2022/day/4)

Part 1:

- The task is to find the number of assignment pairs where one range fully contains the other.
- The input is a list of section assignment pairs, where each pair has a form of x-y indicating a range of section IDs (x to y inclusive) that an elf is assigned to clean. The number of sections that elves are assigned to clean can be different and the section IDs can be larger than single digits.
- The output is the number of pairs where one range fully contains the other. Given two ranges x-y and a-b, one range fully contains the other if and only if x <= a and y >= b.


Part 2:

- The task is to find the number of pairs that overlap at all.
- The input is the same list of section assignment pairs.
- The output is the number of overlapping assignment pairs, where overlapping means that the ranges have a non-zero intersection. Given two ranges x-y and a-b, they overlap if and only if the range (max(x, a), min(y, b)) is not empty.

