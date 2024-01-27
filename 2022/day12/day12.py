import numpy as np
import networkx as nx


def get_ord(x):
    if x == "S":
        return ord("a")
    elif x == "E":
        return ord("z")
    return ord(x)


def day12_1():
    file1 = open("2022/day12/input12_1.txt", "r")
    lines = file1.readlines()
    lines = [l.strip() for l in lines]
    lines = [list(l) for l in lines]

    X = np.array(lines)
    edges = []
    G = nx.DiGraph()
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            node = X[i, j] if X[i, j] in ["S", "E"] else X[i, j] + str(i) + "_" + str(j)
            G.add_node(node)
            for k, m in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
                if i + k >= X.shape[0] or j + m >= X.shape[1] or i + k < 0 or j + m < 0:
                    continue
                node_next = (
                    X[i + k, j + m]
                    if X[i + k, j + m] in ["S", "E"]
                    else X[i + k, j + m] + str(i + k) + "_" + str(j + m)
                )

                if get_ord(X[i + k, j + m]) - get_ord(X[i, j]) <= 1:
                    edges.append((node, node_next, {"weight": 1}))

    G.add_edges_from(edges)

    p1 = nx.shortest_path_length(
        G, source="S", target="E", weight="weight", method="dijkstra"
    )

    print("Solution day 12.1:", p1)


def day12_2():
    file1 = open("2022/day12/input12_1.txt", "r")
    lines = file1.readlines()
    lines = [l.strip() for l in lines]
    lines = [list(l) for l in lines]

    X = np.array(lines)
    edges = []
    G = nx.DiGraph()
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            node = X[i, j] if X[i, j] in ["S", "E"] else X[i, j] + str(i) + "_" + str(j)
            G.add_node(node)
            for k, m in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
                if i + k >= X.shape[0] or j + m >= X.shape[1] or i + k < 0 or j + m < 0:
                    continue
                node_next = (
                    X[i + k, j + m]
                    if X[i + k, j + m] in ["S", "E"]
                    else X[i + k, j + m] + str(i + k) + "_" + str(j + m)
                )

                if get_ord(X[i + k, j + m]) - get_ord(X[i, j]) <= 1:
                    edges.append((node, node_next, {"weight": 1}))

    G.add_edges_from(edges)

    all_path_lengths = []
    for n in G.nodes:
        if "a" in n:
            try:
                p1 = nx.shortest_path_length(
                    G, source=n, target="E", weight="weight", method="dijkstra"
                )
            except:
                continue  # no path found
            all_path_lengths.append(p1)

    print("Solution day 12.2:", min(all_path_lengths))


if __name__ == "__main__":
    day12_1()
    day12_2()
