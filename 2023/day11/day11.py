from itertools import combinations
from itertools import accumulate


def day11():
    grid = [l.strip() for l in open("2023/day11/input.txt", "r").readlines()]
    part_1(grid)
    part_2(grid, n=10**6)


def part_1(grid):
    for _ in range(2):
        grid = [  # naive approach: Transpose grid twice and replicate the empty rows
            l
            for l in list(map(list, zip(*grid)))
            for _ in range((1 + all([ll == "." for ll in l])))
        ]
    galaxies = [(i, j) for i, l in enumerate(grid) for j, c in enumerate(l) if c == "#"]
    dist = [sum(abs(x - y) for x, y in zip(g, h)) for g, h in combinations(galaxies, 2)]
    print(f"Solution Day 11.1: {sum(dist)}")


def part_2(G, n=2):
    idx = lambda g: accumulate([1 + (n - 1) * all([c == "." for c in r]) for r in g])
    r_i, c_i = list(idx(G)), list(idx([l for l in list(map(list, zip(*G)))]))
    P = [(r_i[i], c_i[j]) for i, l in enumerate(G) for j, c in enumerate(l) if c == "#"]
    dist = [sum(abs(x - y) for x, y in zip(g, h)) for g, h in combinations(P, 2)]
    print(f"Solution Day 11.2: {sum(dist)}")


if __name__ == "__main__":
    day11()
