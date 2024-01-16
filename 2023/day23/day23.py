from collections import deque


def brutus(G, from_, target_n, visited, dist=0):
    ans = -1
    for to_ in G[from_].keys() - visited:
        if to_ == target_n:
            return dist + G[from_][target_n]
        ans = max(ans, brutus(G, to_, target_n, visited | {to_}, dist + G[from_][to_]))
    return ans


def day23(part_2=False):
    file1 = open("2023/day23/input.txt", "r")
    lines = [l.strip() for l in file1.readlines()]
    G = [list(l) for l in lines]

    nodes, q, visited, start = dict(), deque(), set(), G[0].index(".")
    directions = [(0, 1, "<"), (0, -1, ">"), (1, 0, "?"), (-1, 0, "v")]
    q.appendleft((0, start, False, 0, start, 0))
    while q:
        y, x, dir, y_start, x_start, dist = q.pop()

        if y != len(G) - 1:
            cnt = sum([G[y + dy][x + dx] != "#" for dy, dx, _ in directions])
        if y == len(G) - 1 or cnt > 2:  # We have a new node or the final node
            from_, to_ = (y_start, x_start), (y, x)
            if from_ not in nodes:
                nodes[from_] = dict()
            nodes[from_][to_] = dist
            if not dir or part_2:  # part 2 does not have any directed edges
                if to_ not in nodes:
                    nodes[to_] = dict()
                nodes[to_][from_] = dist
            y_start, x_start, dir, dist = y, x, False, 0

        if (y, x) in visited:
            continue
        visited.add((y, x))

        if y == len(G) - 1:
            final_node = y, x
            continue

        ns = {"<": [y, x - 1], ">": [y, x + 1], "v": [y + 1, x]}
        if G[y][x] in ns:
            q.appendleft(tuple(ns[G[y][x]] + [True, y_start, x_start, dist + 1]))
            continue

        for dy, dx, v in directions:
            if G[y + dy][x + dx] in "#" + v:
                continue
            q.appendleft((y + dy, x + dx, dir, y_start, x_start, dist + 1))

    # Problem is NP-hard, so we have to brute-force it... (I guess?)
    return brutus(nodes, (0, start), final_node, {(0, start)})


if __name__ == "__main__":
    print(f"Solution Day 23.1: {day23(part_2=False)}")
    print(f"Solution Day 23.2: {day23(part_2=True)}")
