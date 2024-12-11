import numpy as np
import networkx as nx
import time


def solve(G, part, repl=None):
    n = "root"

    for _ in range(10000):
        if n != "root":
            p = tuple(G.predecessors(n))
            assert len(p) == 1
            p = p[0]

        if type(G.nodes[n]["operation"]) is str:
            l, r = tuple(G.successors(n))
            lVal, rVal = G[n][l]["value"], G[n][r]["value"]
            if lVal is not None and rVal is not None:
                # We can complete the operation
                op = G.nodes[n]["operation"]
                expr = str(lVal) + op + str(rVal)
                ans = eval(expr)
                if n == "root" and part == 1:
                    return ans
                elif n == "root" and part == 2:
                    return lVal, rVal

                G[p][n]["value"] = ans

                # Now we can go up one level again...
                n = p
            else:
                if lVal is None:
                    n = l
                if rVal is None:
                    n = r
        elif type(G.nodes[n]["operation"]) is int:
            val = G.nodes[n]["operation"] if repl is None or n != "humn" else repl
            G[p][n]["value"] = val
            n = p
        else:
            raise NotImplementedError()


def day21_1():
    start_time = time.time()
    file1 = open("input21_1.txt", "r")
    lines = file1.readlines()
    lines = [l.strip() for l in lines]
    lines = [l.split(": ") for l in lines]

    edges = []
    G = nx.DiGraph()
    for line in lines:
        node = line[0]
        second = line[1]
        for op in ["*", "+", "-", "/"]:
            if op in second:
                operation = op
                operands = second.split(" " + op + " ")
                for o in operands:
                    edges.append((node, o, {"value": None}))
                break
        else:
            operation = int(second)
        G.add_node(node, operation=operation)

    G.add_edges_from(edges)

    solution1 = solve(G=nx.DiGraph(G), part=1, repl=None)
    print("Solution day 21.1", solution1)

    N = 5
    start, stop = -solution1, solution1  # Not sure yet, what range to choose

    for i in range(1000):
        print("Test range:", (start, stop))
        diffs = []
        vals = np.linspace(start, stop, N)
        for v in vals:
            l, r = solve(nx.DiGraph(G), 2, repl=v)
            diffs.append(l - r)
        diffs = np.array(diffs)
        # Check, how often the error crosses the x-axis
        if i == 0:
            zero_crossings = np.where(np.diff(np.sign(diffs)))[0]
            print("Zero crossings:", zero_crossings)
            assert len(zero_crossings) == 1, (
                "Error: Not exactly one zero crossing detected. "
                "Either you have to widen the start-stop range or "
                "we have a more complex optimization problem that "
                "cannot be solved using this code"
            )

        err = np.abs(diffs).min()
        print("Smallest error: ", err)
        print()
        if err < 1e-7:
            break
        start, stop = (
            vals[diffs == diffs[np.where(diffs > 0)[0]].min()],
            vals[diffs == diffs[np.where(diffs < 0)[0]].max()],
        )
        assert len(start) == 1 and len(stop) == 1
        start, stop = start[0], stop[0]

    print("Total time:", round(time.time() - start_time, 2), "seconds")
    print("Solution day 21.1", solution1)
    print("Solution 21.2:", round(vals[np.abs(diffs).argmin()]))


if __name__ == "__main__":
    day21_1()
