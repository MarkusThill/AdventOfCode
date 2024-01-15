from collections import deque
from functools import cmp_to_key
import numpy as np


def day23():
    file1 = open("2023/day23/example_1.txt", "r")
    lines = [l.strip() for l in file1.readlines()]

    # for part 2:
    # lines = [l.replace("<", ".").replace(">", ".").replace("v", ".") for l in lines]

    print(lines)

    G = [list(l) for l in lines]
    Y, X = len(G), len(G[0])
    start = G[0].index(".")

    # visited = set()
    q = deque()
    q.appendleft((0, start, set()))
    solution_1 = 0
    while q:
        y, x, h = q.pop()
        if (y, x) in h:
            # print("History:", h)
            continue
        if y == Y - 1:
            print("Solution:", len(h))
            solution_1 = max(solution_1, len(h))
            continue
        g = G[y][x]
        if g == "<":
            q.appendleft((y, x - 1, h | {(y, x)}))
            continue
        elif g == ">":
            q.appendleft((y, x + 1, h | {(y, x)}))
            continue
        elif g == "v":
            q.appendleft((y + 1, x, h | {(y, x)}))
            continue
        for dy, dx in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            if G[y + dy][x + dx] == "#":
                continue
            q.appendleft((y + dy, x + dx, h | {(y, x)}))

    print(f"Solution Day 22.1: {solution_1}")
    print(f"Solution Day 22.2: {123}")


if __name__ == "__main__":
    day23()
