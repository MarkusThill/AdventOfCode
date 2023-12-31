from queue import Queue


class Node:
    def __init__(self, x, y, c):
        self.x, self.y, self.c = x, y, c
        self.ends = self.get_ends(c)

    def __str__(self):
        return f"{(self.x, self.y, self.c, self.ends)}"

    def __repr__(self):
        return f"{(self.x, self.y, self.c, self.ends)}"

    def get_ends(self, c):
        return {
            "|": ("n", "s"),
            "-": ("w", "e"),
            "L": ("n", "e"),
            "J": ("n", "w"),
            "7": ("s", "w"),
            "F": ("e", "s"),
            ".": None,
            "S": "S",
        }[c]

    def move(self, in_: str):
        if (self.ends is None) or (in_ not in self.ends):
            raise NotImplementedError(f"Cannot enter the pipe from {in_}")
        out = self.ends[1 - self.ends.index(in_)]
        assert out in {"n", "e", "s", "w"}, f"Wrong out: {out}"
        ret = {"e": (0, 1, "w"), "w": (0, -1, "e"), "n": (-1, 0, "s"), "s": (1, 0, "n")}
        return ret[out]


def find_start(grid):
    """
    Finds the tile on the grid, which is the starting point 'S'.
    """
    return next(((n.x, n.y) for line in grid for n in line if n.c == "S"), None)


def right_neighbors_in_direction_of_travel(n, dx, dy):
    if dx == 1:  # down
        assert n.c not in {"7", "F", "-"}, f"{n, dx, dy}"
    elif dx == -1:  # up
        assert n.c not in {"L", "J", "-"}, f"{n, dx, dy}"
    elif dy == 1:  # right
        assert n.c not in {"L", "F", "|"}, f"{n, dx, dy}"
    elif dy == -1:  # left
        assert n.c not in {"7", "J", "|"}, f"{n, dx, dy}"

    if dx != 0:
        if n.c in {"|"}:
            neighs = {(0, -dx)}
        elif n.c in {"L", "7"}:
            neighs = {(0, -dx), (dx, -dx), (dx, 0)}
        elif n.c in {"J", "F"}:
            neighs = {(-dx, -dx)}
    if dy != 0:
        if n.c in {"-"}:
            neighs = {(dy, 0)}
        elif n.c in {"7", "L"}:
            neighs = {(dy, -dy)}
        elif n.c in {"J", "F"}:
            neighs = {(0, dy), (dy, dy), (dy, 0)}

    assert "neighs" in locals(), f"{n, dx, dy}"
    return {(n.x + ddx, n.y + ddy) for ddx, ddy in neighs}


def day10():
    file1 = open("2023/day10/input_1.txt", "r")
    lines = [l.strip() for l in file1.readlines()]

    grid = [[Node(i, j, c) for (j, c) in enumerate(l)] for (i, l) in enumerate(lines)]

    x_start, y_start = find_start(grid)
    for guess_shape in ["-"]:  # ["|", "L", "J", "7", "F", "-"]:
        try:
            grid[x_start][y_start].c = guess_shape
            for which_end in [1, 0]:
                inside_set = set()
                x, y = x_start, y_start
                n = grid[x][y]
                n.ends = n.get_ends(guess_shape)
                d = n.ends[which_end]
                dx, dy, d = n.move(d)
                n = grid[x + dx][y + dy]
                inside_set |= right_neighbors_in_direction_of_travel(n, dx, dy)
                path = [n]
                while n.x != x_start or n.y != y_start:
                    dx, dy, d = n.move(d)
                    n = grid[n.x + dx][n.y + dy]
                    inside_set |= right_neighbors_in_direction_of_travel(n, dx, dy)
                    path.append(n)
                    assert n.c != "."
            print(f"Found the solution with shape '{guess_shape}'")
            break  # Found a solution
        except NotImplementedError:
            # Guess another pipe shape
            print(f"Pipe shape {guess_shape} did not work!")
            continue
    grid[x_start][y_start].c = "S"

    print(f"Solution Day 10.1: {len(path) // 2}")

    ROWS = len(grid)
    COLS = len(grid[0])
    visited = set()
    while len(inside_set) > 0:
        x, y = inside_set.pop()
        if x >= 0 and x < ROWS and y >= 0 and y < COLS:
            if grid[x][y] not in path:
                grid[x][y].c = "I"
                visited.add((x, y))
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        nx, ny = x + dx, y + dy
                        if (nx, ny) not in visited:
                            inside_set.add((nx, ny))

    counter = 0
    for row in grid:
        for col in row:
            # if col in path:
            #    col.c = "Q"
            if col.c == "I":
                counter += 1
            # print(col.c, end="")
        # print("")

    print(f"Solution Day 10.2: {counter}")


if __name__ == "__main__":
    day10()
