import re
import networkx as nx
import time


def tree2(G, node, valve_state, time_left, elephants_left, transposition):
    if time_left == 0:
        if elephants_left > 0:
            # if also an elephant is supposed to help then use our valve state that we created, since the elephant
            # should not open the same valves as we do...
            return tree2(
                G=G,
                node="AA",
                valve_state=valve_state,
                time_left=26,
                elephants_left=elephants_left - 1,
                transposition=transposition,
            )
        return 0

    key = (node, valve_state, time_left, elephants_left)
    if key in transposition:
        return transposition[key]

    result = 0

    # Open valve if not open yet and if it allows a flow > 0
    if G.nodes[node]["flow"] > 0:
        bit = G.nodes[node]["bit"]
        mask = 1 << bit
        if (valve_state & mask) == 0:  # If valve is not open already...
            flow = G.nodes[node]["flow"]
            result_new = (time_left - 1) * flow + tree2(
                G=G,
                node=node,
                valve_state=valve_state | mask,
                time_left=time_left - 1,
                elephants_left=elephants_left,
                transposition=transposition,
            )
            result = max(result, result_new)

    # Move to another valve
    for s in G.successors(node):
        r = tree2(
            G=G,
            node=s,
            valve_state=valve_state,
            time_left=time_left - 1,
            elephants_left=elephants_left,
            transposition=transposition,
        )
        result = max(result, r)

    transposition[key] = result
    return result


def day16_1_2():
    file1 = open("2022/day16/input16_1.txt", "r")
    lines = file1.readlines()
    lines = [l.strip() for l in lines]
    lines = [l.split("Valve ") for l in lines]
    lines = [l[1] for l in lines]
    lines = [l.split(" has flow rate=") for l in lines]
    nodes = [l[0] for l in lines]
    lines = [l[1].split("; ") for l in lines]
    flows = [int(l[0]) for l in lines]
    lines = [re.split("valve.", l[1]) for l in lines]
    lines = [l[1].strip() for l in lines]
    targets = [l.split(",") for l in lines]
    targets = [[t.strip() for t in l] for l in targets]

    assert len(nodes) == len(flows) and len(flows) == len(targets)

    # create DiGraph
    G = nx.DiGraph()
    bit = 0
    for i, n in enumerate(nodes):
        b = None
        if flows[i] > 0:
            b = bit
            bit += 1
        G.add_node(n, flow=flows[i], bit=b)

    edges = []
    for i, n in enumerate(nodes):
        for suc in targets[i]:
            edges.append((n, suc, {"weight": 1}))

    G.add_edges_from(edges)

    start = time.time()
    ans = tree2(
        G=G,
        node="AA",
        valve_state=0,
        time_left=30,
        elephants_left=0,
        transposition=dict(),
    )
    end = time.time()
    print("Solution day 16.1:", ans, "! Time:", round(end - start, 2), "seconds")

    start = time.time()
    ans = tree2(
        G=G,
        node="AA",
        valve_state=0,
        time_left=26,
        elephants_left=1,
        transposition=dict(),
    )
    end = time.time()
    print("Solution day 16.2:", ans, "! Time:", round(end - start, 2), "seconds")


if __name__ == "__main__":
    day16_1_2()
