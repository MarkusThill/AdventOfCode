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
            "|": ("n", "s"),  # north & south
            "L": ("n", "e"),  # north & east
            "J": ("n", "w"),  # north & west
            "7": ("s", "w"),  # south & west
            "F": ("s", "e"),  # south & east
            "-": ("w", "e"),  # west & east
            ".": None,
            "S": None,
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
    if (
        (dx == 1 and n.c in {"7", "F", "-"})
        or (dx == -1 and n.c in {"L", "J", "-"})
        or (dy == 1 and n.c in {"L", "F", "|"})
        or (dy == -1 and n.c in {"7", "J", "|"})
    ):
        raise NotImplementedError(f"{n, dx, dy}")

    if n.c in {"-", "|"}:
        neighs = {(dy, -dx)}
    elif (dx != 0 and n.c in {"L", "7"}) or (dy != 0 and n.c in {"J", "F"}):
        neighs = {(0, dy - dx), (dx + dy, 0), (dy + dx, dy - dx)}
    elif (dx != 0 and n.c in {"J", "F"}) or (dy != 0 and n.c in {"L", "7"}):
        neighs = {(dy - dx, -dy - dx)}

    assert "neighs" in locals(), f"{n, dx, dy}"
    return {(n.x + ddx, n.y + ddy) for ddx, ddy in neighs}


def day10():
    file1 = open("2023/day10/input_1.txt", "r")
    lines = [l.strip() for l in file1.readlines()]
    grid = [[Node(i, j, c) for (j, c) in enumerate(l)] for (i, l) in enumerate(lines)]

    x_start, y_start = find_start(grid)
    for start_shape_guess in ["|", "L", "J", "7", "F", "-"]:
        try:
            grid[x_start][y_start].c = start_shape_guess
            for which_end in [1, 0]:
                inside_set = set()
                x, y = x_start, y_start
                n = grid[x][y]
                n.ends = n.get_ends(start_shape_guess)
                d = n.ends[which_end]
                # dx, dy, d = n.move(d)
                # n = grid[x + dx][y + dy]
                # inside_set |= right_neighbors_in_direction_of_travel(n, dx, dy)
                # path = [n]
                path = list()
                while n.x != x_start or n.y != y_start or len(path) == 0:
                    dx, dy, d = n.move(d)
                    n = grid[n.x + dx][n.y + dy]
                    inside_set |= right_neighbors_in_direction_of_travel(n, dx, dy)
                    path.append(n)
                    # assert n.c != "."
            print(f"Found solution with pipe '{start_shape_guess}' for start 'S'!")
            break  # Found a solution while walking in both directions
        except NotImplementedError:
            print(f"Pipe shape {start_shape_guess} did not work!")
            continue  # Guess another pipe shape
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

    counter = sum(col.c == "I" for row in grid for col in row)

    print(f"Solution Day 10.2: {counter}")


if __name__ == "__main__":
    day10()
