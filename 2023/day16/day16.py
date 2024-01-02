def compute_energy(grid, beam_start):
    ROWS, COLS = len(grid), len(grid[0])
    beams, all_states, energy = [beam_start], set(), set()

    while len(beams) > 0:
        b = beams.pop()
        while 0 <= b[0] < ROWS and 0 <= b[1] < COLS and b not in all_states:
            all_states.add(b)
            x, y, dx, dy = b
            energy.add((x, y))
            c = grid[x][y]
            if c == "/":
                dx, dy = -dy, -dx
            elif c == "\\":
                dx, dy = dy, dx
            elif c == "-" and dx != 0:
                dx, dy = 0, dx
                beams.append((x, y - dy, dx, -dy))
            elif c == "|" and dy != 0:
                dx, dy = dy, 0
                beams.append((x - dx, y, -dx, dy))
            b = x + dx, y + dy, dx, dy
    return len(energy)


def day16():
    file1 = open("2023/day16/input.txt", "r")
    lines = [l.strip() for l in file1.readlines()]
    grid = [list(l) for l in lines]
    energy = compute_energy(grid, (0, 0, 0, 1))
    print(f"Solution Day 15.1: {energy}")

    # Part 2:
    ROWS, COLS = len(grid), len(grid[0])
    left_col = [(i, 0, 0, 1) for i in range(ROWS)]
    right_col = [(i, COLS - 1, 0, -1) for i in range(ROWS)]
    top_row = [(0, i, 1, 0) for i in range(COLS)]
    bottom_row = [(ROWS - 1, i, -1, 0) for i in range(COLS)]
    all_starts = left_col + right_col + top_row + bottom_row
    all_energies = [compute_energy(grid, b) for b in all_starts]
    print(f"Solution Day 15.2: {max(all_energies)}")


if __name__ == "__main__":
    day16()
