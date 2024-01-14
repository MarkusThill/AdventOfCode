from collections import deque
from functools import cmp_to_key
import numpy as np


def compare_z(item_1, item_2):
    return min(item_1[-1][0], item_1[-1][1]) - min(item_2[-1][0], item_2[-1][1])


def collides(brick1, brick2):
    axes = [  # checks for a collision between two bricks
        [(c2[0] <= c1[0] <= c2[1]) or (c2[0] <= c1[1] <= c2[1]) for c1, c2 in G]
        for G in [zip(brick1, brick2), zip(brick2, brick1)]
    ]
    return all(x or y for x, y in zip(*axes))


def find_supporters(brick, brick_set):
    x, y, z = brick
    brick = (x, y, (z[0] - 1, z[1] - 1))
    return {b for b in brick_set if collides(brick, b)}


def day22():
    file1 = open("2023/day22/input.txt", "r")
    lines = [l.strip() for l in file1.readlines()]

    bricks = [l.split("~") for l in lines]
    bricks = [
        tuple([(int(x), int(y)) for x, y in zip(r[0].split(","), r[1].split(","))])
        for r in bricks
    ]

    max_x, max_y = max(b[0][-1] for b in bricks), max(b[1][-1] for b in bricks)
    height_map = np.ones((max_x + 1, max_y + 1), dtype="int")
    settled, support_bricks, brick_idx, solution_2 = set(), set(), 0, 0
    supports, supported_by = dict(), dict()

    bricks = sorted(bricks, key=cmp_to_key(compare_z))
    while brick_idx < len(bricks):
        x, y, z = b = bricks[brick_idx]
        z_height = z[1] - z[0]

        r_x, r_y = range(x[0], x[1] + 1), range(y[0], y[1] + 1)
        new_z = height_map[r_x, r_y].max()
        height_map[r_x, r_y] = new_z + z_height + 1
        b = x, y, (new_z, new_z + z_height)

        supps = find_supporters(b, settled)  # Find supporting bricks underneath
        settled.add(b)
        brick_idx += 1

        for s in supps:  # For part 2: s supports b
            if s not in supports:
                supports[s] = set()
            supports[s].add(b)
        supported_by[b] = supps  # For part 2: b supported-by s

    # Part 2:
    for b in settled:
        q, falling = deque(), {b}
        q.extend(supports[b] if b in supports else [])
        while q:
            b = q.pop()
            if supported_by[b].issubset(falling):
                falling.add(b)
                q.extend(supports[b] if b in supports else [])
        solution_2 += len(falling) - 1

    support_bricks = set([list(s)[0] for s in supported_by.values() if len(s) == 1])
    print(f"Solution Day 22.1: {len(bricks) - len(support_bricks)}")
    print(f"Solution Day 22.2: {solution_2}")


if __name__ == "__main__":
    day22()
