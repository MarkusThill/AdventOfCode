class Node:
    def __init__(self, x, y, c):
        self.x, self.y, self.c, self.ends = x, y, c, self.get_ends(c)

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
        assert (
            self.ends is not None and in_ in self.ends
        ), f"Cannot enter the pipe from {in_}"
        out = self.ends[1 - self.ends.index(in_)]
        ret = {"e": (0, 1, "w"), "w": (0, -1, "e"), "n": (-1, 0, "s"), "s": (1, 0, "n")}
        return ret[out]


def find_start(grid):
    return next(((n.x, n.y) for line in grid for n in line if n.c == "S"), None)


def right_neighbors_in_direction_of_travel(n, dx, dy):
    assert not (
        (dx == 1 and n.c in {"7", "F", "-"})
        or (dx == -1 and n.c in {"L", "J", "-"})
        or (dy == 1 and n.c in {"L", "F", "|"})
        or (dy == -1 and n.c in {"7", "J", "|"})
    ), f"node {n.c} and direction {dx, dy}!"

    if n.c in {"-", "|"}:
        neighs = {(dy, -dx)}
    elif (dx != 0 and n.c in {"L", "7"}) or (dy != 0 and n.c in {"J", "F"}):
        neighs = {(0, dy - dx), (dx + dy, 0), (dy + dx, dy - dx)}
    elif (dx != 0 and n.c in {"J", "F"}) or (dy != 0 and n.c in {"L", "7"}):
        neighs = {(dy - dx, -dy - dx)}
    return {(n.x + ddx, n.y + ddy) for ddx, ddy in neighs}


def day10():
    file1 = open("2023/day10/input_1.txt", "r")
    lines = [l.strip() for l in file1.readlines()]
    grid = [[Node(i, j, c) for j, c in enumerate(l)] for i, l in enumerate(lines)]
    n_rows, n_cols, x_start, y_start = len(grid), len(grid[0]), *find_start(grid)
    for start_shape_guess in ["|", "L", "J", "7", "-", "F"]:
        try:
            grid[x_start][y_start].c = start_shape_guess
            pipe_loop, loop_neighbors = list(), set()
            n = grid[x_start][y_start]
            n.ends = n.get_ends(start_shape_guess)
            d = n.ends[1]  # direction: the end of the pipe that we leave (0 or 1)
            while n.x != x_start or n.y != y_start or len(pipe_loop) == 0:
                dx, dy, d = n.move(d)
                n = grid[n.x + dx][n.y + dy]
                loop_neighbors |= right_neighbors_in_direction_of_travel(n, dx, dy)
                pipe_loop.append(n)
        except AssertionError:
            continue  # Guess another pipe shape for 'S'
        break  # Found a solution

    solution_1 = len(pipe_loop) // 2
    print(f"Solution Day 10.1: {solution_1} (pipe shape '{start_shape_guess}' for 'S')")

    # Part 2:
    Q, visited, is_outside = [-1, 0, 1], set(), False
    while len(loop_neighbors) > 0:
        x, y = loop_neighbors.pop()
        if 0 <= x < n_rows and 0 <= y < n_cols and grid[x][y] not in pipe_loop:
            visited.add((x, y))
            loop_neighbors |= {(x + dx, y + dy) for dx in Q for dy in Q} - visited
        is_outside |= x < 0 or y < 0  # Flood-Fill: Either got the inside or outside.

    solution_2 = (
        n_rows * n_cols - len(visited) - len(pipe_loop) if is_outside else len(visited)
    )
    print(f"Solution Day 10.2: {solution_2}")


if __name__ == "__main__":
    day10()
