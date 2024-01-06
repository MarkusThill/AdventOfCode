import queue


def shoelace(points):
    """
    https://en.wikipedia.org/wiki/Shoelace_formula
    """
    xx, yy = zip(*points)
    return (
        sum(
            [
                s1 - s2
                for s1, s2 in zip(
                    [x * y for x, y in zip(xx, list(yy[1:]) + [yy[0]])],
                    [x * y for x, y in zip(list(xx[1:]) + [xx[0]], yy)],
                )
            ]
        )
    ) // 2


def day18():
    file1 = open("2023/day18/input.txt", "r")
    lines = [l.strip() for l in file1.readlines()]
    lines = [l.split(" ") for l in lines]

    # Part 1:
    points, perimeter = parse_part_1(lines)

    # If we draw the points (x,y) into the center of each corresponding 1x1 block, we
    # can see that we are missing some of the area. We can simply move the whole shape
    # down & left by half a box to illustrate this. We will see that half (+1) of the
    # 'trench' (perimeter) is missing. Hence, we add it here. This is somewhat related
    # to Pick's theorem: https://en.wikipedia.org/wiki/Pick%27s_theorem
    print(f"Solution Day 18.1: {abs(shoelace(points)) + perimeter // 2 + 1}")

    # Part 2:
    points, perimeter = parse_part_2(lines)
    print(f"Solution Day 18.2: {abs(shoelace(points)) + perimeter // 2 + 1}")


def parse_part_1(lines):
    x, y = 0, 0
    points, perimeter = [(x, y)], 0
    for d, v, _ in lines:
        v = int(v)
        perimeter += v
        if d == "R":
            x, y = x + v, y
        elif d == "L":
            x, y = x - v, y
        elif d == "U":
            x, y = x, y + v
        elif d == "D":
            x, y = x, y - v
        points.append((x, y))
    return points, perimeter


def parse_part_2(lines):
    x, y = 0, 0
    points, perimeter = [(x, y)], 0
    for _, _, c in lines:
        v, d = int(c[2:-2], 16), c[-2]
        perimeter += v
        if d == "0":
            x, y = x + v, y
        elif d == "2":
            x, y = x - v, y
        elif d == "3":
            x, y = x, y + v
        elif d == "1":
            x, y = x, y - v
        points.append((x, y))
    return points, perimeter


if __name__ == "__main__":
    day18()
