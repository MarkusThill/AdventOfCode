from __future__ import annotations

from collections import deque
from collections import defaultdict
import math


def day11_1(
    path: str = "2025/day11/input_1.txt",
    start_node: str = "you",
    end_node: str = "out",
) -> int:
    """Count directed routes from a start node to an end node using brute-force BFS expansion.

    The input file is interpreted as a directed graph, where each line defines a node
    and its outgoing edges in the form::

        node: neighbor1 neighbor2 neighbor3

    The algorithm performs a breadth-first expansion starting from ``start_node``.
    Each time ``end_node`` is reached, a path is counted. Instead of storing full paths,
    only the current node is tracked in the queue; this works because the graph is assumed
    to be acyclic, ensuring that the expansion terminates.

    This approach explicitly enumerates all possible routes and is therefore simple and
    easy to reason about, but potentially inefficient for large graphs. It is intended
    as a straightforward solution rather than an optimized one.

    Args:
        path: Path to the input file describing the directed graph.
        start_node: Name of the node where all routes start.
        end_node: Name of the node where routes are counted.

    Returns:
        The total number of distinct directed routes from ``start_node`` to ``end_node``.
    """
    # Build adjacency list: node -> list of outgoing neighbors
    graph: dict[str, list[str]] = {}

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            # Split only once to allow arbitrary spacing on the right-hand side
            node, rhs = line.strip().split(":", 1)

            # `split()` (without argument) handles multiple spaces robustly
            graph[node] = rhs.strip().split()

    # Queue holds the current frontier of nodes to expand
    q: deque[str] = deque([start_node])

    # Counts how many times we reach the end node
    path_counter = 0

    # Standard BFS-style loop: expand nodes until no routes remain
    while q:
        n = q.popleft()

        # Reaching the end node corresponds to one complete route
        if n == end_node:
            path_counter += 1
            continue

        # Expand the current node by enqueueing all outgoing neighbors
        # Assumption: every node has an outgoing list defined in the input.
        q.extend(graph[n])

    return path_counter


def day11_2(
    path: str = "2025/day11/input_1.txt",
    checkpoints: list[tuple[str, str]] | None = None,
) -> int:
    """Compute the product of path counts for selected DAG segments using topological DP.

    A quick inspection of the input graph reveals important structural properties:
    - The node ``"svr"`` has no incoming edges and therefore must be the global start.
    - All valid routes to the final node ``"out"`` must pass through the intermediate
      nodes ``"fft"`` and ``"dac"`` in this fixed order::

          svr → ... → fft → ... → dac → ... → out

    This observation allows the overall path count to be decomposed into independent
    path-counting segments (e.g. ``svr → fft``, ``fft → dac``, ``dac → out``), whose
    individual counts can be multiplied to obtain the final result. The correctness
    of the final segment (``dac → out``) can also be verified independently using
    ``day11_1()``.

    The function reads a directed acyclic graph (DAG) from ``path``, where each line
    has the form::

        node: child1 child2 child3

    The algorithm proceeds as follows:

      1. Parse the file into an adjacency list and collect all nodes (including
         sink nodes that appear only as children, such as ``"out"``).
      2. Compute a topological ordering of the DAG using Kahn's algorithm in
         O(V + E) time.
      3. For each ``(start_node, end_node)`` pair in ``checkpoints``, run a dynamic
         programming pass along the topological order to count all directed paths
         from ``start_node`` to ``end_node``.
      4. Multiply the path counts of all segments to obtain the final result.

    This approach avoids explicitly enumerating all paths.

    Args:
        path: Path to the input file describing the directed acyclic graph.
        checkpoints: List of ``(start_node, end_node)`` pairs defining the path
            segments to evaluate. If ``None``, defaults to::

                [("svr", "fft"), ("fft", "dac"), ("dac", "out")]

    Returns:
        The product of the number of distinct directed paths for each segment
        specified in ``checkpoints``.

    Raises:
        ValueError: If the graph is not a DAG (i.e., a cycle is detected during
            topological sorting).
    """
    # If no explicit path segments are provided, use the known fixed chain.
    # Each tuple (start, end) means: "count paths from start to end".
    if checkpoints is None:
        checkpoints = [("svr", "fft"), ("fft", "dac"), ("dac", "out")]

    # ----------------------------------------------------------------------
    # Parse the input file and build the adjacency list representation
    # ----------------------------------------------------------------------
    # `graph` maps each node to a tuple of its outgoing neighbors.
    # `nodes` collects *all* nodes that appear anywhere (as parent or child).
    graph: dict[str, tuple[str, ...]] = {}
    nodes: set[str] = set()

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            # Each line has the form:
            #     node: child1 child2 child3
            #
            # We split only once at ":", so spacing on the RHS does not matter.
            u, rhs = line.strip().split(":", 1)
            u = u.strip()

            # split() (without arguments) collapses multiple spaces safely.
            vs = tuple(rhs.strip().split())

            # Store outgoing edges
            graph[u] = vs

            # Track all nodes seen so far
            nodes.add(u)
            nodes.update(vs)

    # Some nodes (e.g. the final sink "out") appear only as children and
    # never as a left-hand-side node in the file.
    #
    # For topological sorting and DP, every node must exist as a key
    # in the adjacency list. Sink nodes therefore get an empty tuple.
    for n in nodes:
        if n not in graph:
            graph[n] = ()

    # ----------------------------------------------------------------------
    # Compute a topological order using Kahn's algorithm
    # ----------------------------------------------------------------------
    # indeg[n] = number of incoming edges into node n
    indeg: dict[str, int] = {n: 0 for n in nodes}

    # Count incoming edges by scanning all adjacency lists
    for u, vs in graph.items():
        for v in vs:
            indeg[v] += 1

    # Initialize queue with all nodes that have no incoming edges.
    # These nodes can safely appear first in topological order.
    q: deque[str] = deque([n for n, d in indeg.items() if d == 0])

    # Will hold the final topological ordering
    topo: list[str] = []

    while q:
        # Take a node whose dependencies are already satisfied
        u = q.popleft()
        topo.append(u)

        # "Remove" u from the graph by decrementing the indegree
        # of all nodes it points to.
        for v in graph[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)

    # If not all nodes were processed, the graph contains a cycle,
    # which violates the DAG assumption required for this approach.
    if len(topo) != len(nodes):
        raise ValueError(
            "Graph is not a DAG (cycle detected), cannot topologically sort."
        )

    # Precompute index positions in the topo order.
    # This avoids expensive topo.index(...) calls later (O(V) each).
    pos: dict[str, int] = {n: i for i, n in enumerate(topo)}

    # ----------------------------------------------------------------------
    # For each (start, end) segment, count paths using DP and multiply results
    # ----------------------------------------------------------------------
    product = 1

    for start_node, end_node in checkpoints:
        # Look up positions of the segment endpoints in topological order
        start_i = pos[start_node]
        end_i = pos[end_node]

        # In a DAG, if end appears before start in topo order,
        # there cannot be any path from start to end.
        if end_i < start_i:
            return 0

        # ways[x] = number of ways to reach node x from start_node
        ways: dict[str, int] = defaultdict(int)
        ways[start_node] = 1  # exactly one way to start at the start node

        # Propagate path counts forward along the topo order,
        # but only in the relevant slice [start_i, end_i).
        for u in topo[start_i:end_i]:
            wu = ways[u]

            # If u is unreachable, it contributes nothing downstream
            if wu == 0:
                continue

            # Every path that reaches u can be extended to each child v
            for v in graph[u]:
                ways[v] += wu

        # Multiply the number of paths for this segment into the final result
        product *= ways[end_node]

    return product


if __name__ == "__main__":
    result_1 = day11_1()  # "2025/day11/example_1.txt"
    assert result_1 == 683, f"Real: {result_1} vs. Expected: {683}"
    print("Solution for day11.1:", result_1)

    result_2 = day11_2()  # "2025/day11/example_2.txt"
    print("Solution for day11.2:", result_2)
    assert result_2 == 533996779677200, (
        f"Real: {result_2} vs. Expected: {533996779677200}"
    )


def day11_2_old(
    path: str = "2025/day11/input_1.txt",
    all_paths=[("svr", "fft"), ("fft", "dac"), ("dac", "out")],
) -> int:
    """
    Prototyp for day 02.
    """
    with open(path, "r", encoding="utf-8") as f:
        nodes, outs = zip(*[line.strip().split(":") for line in f])

    outs = [o.strip().split(" ") for o in outs]

    graph = {}
    for n, o in zip(nodes, outs):
        graph[n] = set(o)

    # Implementation of Kahn's algorithm (bit inefficient)
    kahns_graph = graph.copy()
    topological_order = []
    while kahns_graph:
        nodes_with_parents = {p for parents in kahns_graph.values() for p in parents}
        root_nodes = set(kahns_graph.keys()) - nodes_with_parents
        topological_order.extend(root_nodes)
        for k in root_nodes:
            del kahns_graph[k]

    all_path_way_lengths = {}
    for start_node, end_node in all_paths:
        index_start = topological_order.index(start_node)

        ways = defaultdict(int)
        ways[start_node] = 1

        for t in topological_order[index_start:]:
            if t == end_node:
                break  # No need to compute the ways to child nodes of our target
            for child in graph[t]:
                ways[child] += ways[t]
        all_path_way_lengths[(start_node, end_node)] = ways[end_node]

    return math.prod(all_path_way_lengths.values())
