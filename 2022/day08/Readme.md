# --- Day 8: Treetop Tree House ---

You can find the original problem statement here: [https://adventofcode.com/2022/day/8](https://adventofcode.com/2022/day/8)

Day 8 Part 1: Given a map of trees represented by a grid of digits, where each digit represents the height of a tree, determine the number of trees that are visible from outside the grid when looking directly along a row or column. A tree is visible if all of the other trees between it and an edge of the grid are shorter than it. Only consider trees in the same row or column.

Day 8 Part 2: Given the same map of trees, measure the viewing distance from a given tree. Look up, down, left, and right from that tree, stop if you reach an edge or at the first tree that is the same height or taller than the tree under consideration. A tree's scenic score is found by multiplying together its viewing distance in each of the four directions. Consider each tree on your map, find the highest scenic score possible.