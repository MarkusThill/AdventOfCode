from collections import deque
from functools import cmp_to_key
import numpy as np


def compare_z(item_1, item_2):
    return min(item_1[-1][0], item_1[-1][1]) - min(item_2[-1][0], item_2[-1][1])


def collides(brick1, brick2):
    axes = [
        [(c2[0] <= c1[0] <= c2[1]) or (c2[0] <= c1[1] <= c2[1]) for c1, c2 in G]
        for G in [zip(brick1, brick2), zip(brick2, brick1)]
    ]
    # print(list(zip(*axes)))
    # return any(all(a) for a in axes)
    return all([x or y for x, y in zip(*axes)])


def collides_any(brick, brick_set):
    supporters = set()
    for b in brick_set:
        assert collides(brick, b) == collides(b, brick), f"\n{brick}\n{b}"
        if collides(brick, b):
            supporters.add(b)
        # if len(supporters) > 1:
        #    break
    return supporters


def day22():
    file1 = open("2023/day22/input.txt", "r")
    lines = [l.strip() for l in file1.readlines()]

    bricks = [l.split("~") for l in lines]
    bricks = [
        tuple([(int(x), int(y)) for x, y in zip(r[0].split(","), r[1].split(","))])
        for r in bricks
    ]

    max_x, max_y = max(b[0][-1] for b in bricks), max(b[1][-1] for b in bricks)
    print(max_x, max_y)
    height_map = np.ones((max_x + 1, max_y + 1), dtype="int")

    settled, support_bricks = set(), set()
    supports = dict()

    while len(settled) != len(bricks):
        # TODO: Sort Can be moved outside loop:
        bricks = sorted(bricks, key=cmp_to_key(compare_z))
        for i, b in enumerate(bricks):
            if b not in settled:
                break
        x, y, z = b
        z_height = z[1] - z[0]

        r_x, r_y = range(x[0], x[1] + 1), range(y[0], y[1] + 1)
        new_z = height_map[r_x, r_y].max()
        height_map[r_x, r_y] = new_z + z_height + 1
        b = x, y, (new_z, new_z + z_height)

        # s = collides_any(b, settled)
        # assert len(s) == 0

        # Find supporting bricks underneath
        bb = x, y, (new_z - 1, new_z + z_height - 1)
        s = collides_any(bb, settled)
        if len(s) == 1:
            # b_depends_on = s[0]
            support_bricks.add(list(s)[0])
            # if b_depends_on not in supports:
            #    supports[b_depends_on] = set()
            # supports[b_depends_on].add(b)
        # if len(s) == 0 and bb[-1][0] > 1:
        #    print("DEBUG:", old_b, bb, s)
        #    for x in bricks[:i]:
        #        print(x)
        #    return

        bricks[i] = b
        settled.add(b)

    # for n, b in zip("ABCDEFG", bricks):
    #    counter = 0
    #    q = deque()
    #    q.appendleft(b)
    #    while q:
    #        bb = q.pop()
    #        if bb not in supports:
    #            print(bb)
    #            continue
    #        b_supports = supports[bb]
    #        counter += len(b_supports)
    #        for e in b_supports:
    #            q.appendleft(e)
    #    print(n, b, counter)
    # print(supports[bricks[0]])

    if False:
        grid = ["..."] * 10
        for n, b in zip("ABCDEFG", bricks):
            x, y, z = b
            for xx in range(x[0], x[1] + 1):
                for zz in range(z[0], z[1] + 1):
                    print(zz)
                    rr = list(grid[zz])
                    if rr[xx] != ".":
                        rr[xx] = "?"
                    else:
                        rr[xx] = n
                    grid[zz] = "".join(rr)

        for g in reversed(grid):
            print(g)

    print(f"Solution Day 22.1: {len(bricks) - len(support_bricks)}")
    print(f"Solution Day 22.2: {123}")


if __name__ == "__main__":
    # x1 = ((1, 4), (8, 8), (3, 3))
    # x2 = ((3, 3), (7, 9), (3, 3))
    # print(collides(x1, x2))
    day22()


def day22_old():
    file1 = open("2023/day22/input.txt", "r")
    lines = [l.strip() for l in file1.readlines()]

    bricks = [l.split("~") for l in lines]
    bricks = [
        tuple([(int(x), int(y)) for x, y in zip(r[0].split(","), r[1].split(","))])
        for r in bricks
    ]

    settled = set()
    support = set()
    settled_z_max = 0
    while len(settled) != len(bricks):
        bricks = sorted(bricks, key=cmp_to_key(compare_z))
        # print("bricks:", bricks)
        for i, b in enumerate(bricks):
            if b not in settled:
                break

        # Check if this brick collides with already settled bricks
        assert len(collides_any(b, settled)) == 0, f"{settled, b, i}"
        b_height = b[-1][1] - b[-1][0]
        b = b[0], b[1], (settled_z_max, settled_z_max + b_height)
        while True:
            z1, z2 = b[-1][0] - 1, b[-1][1] - 1
            new_b = b[0], b[1], (z1, z2)
            collisions = collides_any(new_b, settled)
            if len(collisions) > 0 or z1 < 1 or z2 < 1:
                if len(collisions) == 1:
                    support |= collisions
                break
            b = new_b
        bricks[i] = b
        settled.add(b)
        settled_z_max = max(settled_z_max, b[-1][1] + 10)
        print(settled_z_max)
        print("Done with", i, "out of", len(bricks))

    if False:
        grid = ["..."] * 10
        for n, b in zip("ABCDEFG", bricks):
            x, y, z = b
            for xx in range(y[0], y[1] + 1):
                for zz in range(z[0], z[1] + 1):
                    print(zz)
                    rr = list(grid[zz])
                    if rr[xx] != ".":
                        rr[xx] = "?"
                    else:
                        rr[xx] = n
                    grid[zz] = "".join(rr)

        for g in reversed(grid):
            print(g)

    assert len(settled) == len(bricks)
    print(len(settled) - len(support))

    print(f"Solution Day 22.1: {len(settled) - len(support)}")
    print(f"Solution Day 22.2: {123}")
