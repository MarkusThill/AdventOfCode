from heapq import heappush, heappop


def bfs(G, pos=(0, 0), d=(0, 1), max_budget=3, min_moves_dir=0, target=None):
    ROWS, COLS = len(G), len(G[0])
    target = ROWS - 1, COLS - 1 if target is None else target
    x, y, dx, dy, cost = *pos, *d, 0

    Q, visited = [], set()
    heappush(Q, (cost, x, y, dx, dy, max_budget))  # initial state...
    while len(Q) > 0:
        # We always pop the state with the lowest cost so far
        # This idea is somehow similar to what is done in Dijkstra's algorithm
        state = heappop(Q)
        cost, x, y, dx, dy, budget = state
        if state[1:] in visited:
            continue  # We already have the optimal cost for this state...
        visited.add(state[1:])
        moves_dir = max_budget - budget  # num. of consecutive moves in one direction
        if (x, y) == target and moves_dir >= min_moves_dir:
            return cost  # Found the target cell. Make sure that we previously made at least X moves

        # Generate all possible afterstates (straight, turn-left, turn-right)
        all_moves = [(dx, dy, 1), (-dy, dx, 0), (dy, -dx, 0)]
        moves = all_moves if moves_dir >= min_moves_dir else [(dx, dy, 1)]
        for ndx, ndy, nb in moves:
            nx, ny = (x + ndx, y + ndy)
            # Only allow the previous direction, if we did not reach the maximum # of moves in one direction
            if budget - nb >= 0 and 0 <= nx < ROWS and 0 <= ny < COLS:
                nb, nc = budget - 1 if nb else max_budget - 1, cost + G[nx][ny]
                heappush(Q, (nc, nx, ny, ndx, ndy, nb))

    return None  # We should not arrive here...


def day17():
    file1 = open("2023/day17/input.txt", "r")
    lines = [l.strip() for l in file1.readlines()]
    grid = [[int(ll) for ll in list(l)] for l in lines]

    print(f"Solution Day 17.1: {bfs(grid)}")
    print(f"Solution Day 17.2: {bfs(grid, max_budget=10, min_moves_dir=4)}")


if __name__ == "__main__":
    day17()
