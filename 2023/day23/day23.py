from collections import deque


def brutus(nodes, from_, target_n, visited, dist=0):
    ans = -1
    for to_ in nodes[from_].keys():
        if to_ in visited:
            continue
        if to_ == target_n:
            return dist + nodes[from_][target_n]
        val = brutus(nodes, to_, target_n, visited | {to_}, dist + nodes[from_][to_])
        ans = max(ans, val)

    return ans


def day23():
    file1 = open("2023/day23/input.txt", "r")
    lines = [l.strip() for l in file1.readlines()]
    # lines = [l.replace("<", ".").replace(">", ".").replace("v", ".") for l in lines]
    # print(lines)

    G = [list(l) for l in lines]
    Y, X = len(G), len(G[0])
    start = G[0].index(".")

    nodes = dict()
    visited = set()
    q = deque()
    q.appendleft((0, start, False, 0, start, 0))
    directions = [(0, 1, "<"), (0, -1, ">"), (1, 0, "?"), (-1, 0, "v")]
    while q:
        y, x, dir, y_start, x_start, dist = state = q.pop()

        if y != Y - 1:
            cnt = [G[y + dy][x + dx] != "#" for dy, dx, _ in directions]
        if y == Y - 1 or sum(cnt) > 2:  # We have a new node or the final node
            from_, to_ = (y_start, x_start), (y, x)
            # assert from_[0] < Y and from_[1] < X
            # assert to_[0] < Y and to_[1] < X
            if from_ not in nodes:
                nodes[from_] = dict()
            nodes[from_][to_] = dist
            if not dir or True:  # no directed edge
                if to_ not in nodes:
                    nodes[to_] = dict()
                nodes[to_][from_] = dist
            y_start, x_start, dir, dist = y, x, False, 0

        if (y, x) in visited:
            continue
        visited.add((y, x))

        if y == Y - 1:
            final_node = y, x
            continue

        g = G[y][x]
        if g == "<":
            q.appendleft((y, x - 1, True, y_start, x_start, dist + 1))
            continue
        elif g == ">":
            q.appendleft((y, x + 1, True, y_start, x_start, dist + 1))
            continue
        elif g == "v":
            q.appendleft((y + 1, x, True, y_start, x_start, dist + 1))
            continue

        for dy, dx, v in directions:
            if G[y + dy][x + dx] == "#" or G[y + dy][x + dx] == v:
                continue
            q.appendleft((y + dy, x + dx, dir, y_start, x_start, dist + 1))

    # print(sum([len(n) for n in nodes]), nodes)
    # print()

    print(f"Solution Day 22.1: {123}")
    print(f"Solution Day 22.2: {brutus(nodes, (0, start), final_node, {(0, start)})}")


if __name__ == "__main__":
    day23()
