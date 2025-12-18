from __future__ import annotations

from itertools import combinations
import math
from typing import Iterable
import heapq


class TopKSets:
    """Maintain the k largest sets seen so far (by cardinality).

    This class implements a small fixed-size *min-heap* to track the
    largest `k` sets based on their length. Each set is considered
    at most once, determined by *object identity* (not by equality).

    This implementation is primarily intended for educational purposes.
    It demonstrates how a heap can be used to maintain a running top-k
    selection, but it assumes that sets do not change size after being
    considered.

    Attributes:
        k: Number of largest sets to retain.
        _heap: Min-heap storing tuples of the form
            ``(len(set), id(set), set)``.
        _seen: Set of object IDs already considered, used to enforce
            identity-based uniqueness.
    """

    def __init__(self, k: int = 3) -> None:
        """Initialize an empty top-k tracker.

        Args:
            k: Number of largest sets to keep.
        """
        self.k = k
        self._heap: list[tuple[int, int, set]] = []  # (size, id, set)
        self._seen: set[int] = set()  # ids already inserted

    def consider(self, s: set) -> None:
        """Consider a set for inclusion in the top-k.

        If the set has already been considered (based on object identity),
        it is ignored. Otherwise, the set is inserted into the internal
        heap if:

        - fewer than `k` sets have been seen so far, or
        - the set is strictly larger than the smallest set currently
          stored in the top-k heap.

        Args:
            s: The set to consider.
        """
        oid = id(s)
        if oid in self._seen:
            return  # already considered

        self._seen.add(oid)
        item = (len(s), oid, s)

        if len(self._heap) < self.k:
            heapq.heappush(self._heap, item)
            return

        # Replace smallest-of-top-k if strictly larger
        if item[0] > self._heap[0][0]:
            heapq.heapreplace(self._heap, item)

    def top(self) -> list[set]:
        """Return the current top-k sets.

        Returns:
            A list of sets sorted from largest to smallest by size.
        """
        return [s for _, _, s in sorted(self._heap, reverse=True)]


def day08_1_slow(
    path: str = "2025/day08/input_1.txt", n_connections: int = 1000
) -> int:
    """Solve Day 08, Part 1 using an explicit set-merging approach.

    This reference implementation builds connected components ("circuits")
    by repeatedly merging Python `set` objects. Initially, each junction
    box forms its own singleton circuit. The `n_connections` shortest
    pairwise distances are then processed, and the corresponding circuits
    are merged by taking set unions.

    While conceptually simple and useful for educational purposes, this
    approach is computationally expensive:

    - All pairwise distances are computed and fully sorted
      (O(n² log n)).
    - Circuit merging requires repeatedly materializing new sets and
      relabeling all members (O(size of circuit) per merge).

    The final result is computed by selecting the three largest circuits
    and returning the product of their sizes.

    Args:
        path: Path to the input file containing one junction box per line
            as comma-separated coordinates.
        n_connections: Number of shortest connections to process.

    Returns:
        The product of the sizes of the three largest circuits.
    """
    with open(path, "r", encoding="utf-8") as f:
        rows = [line.rstrip("\n") for line in f]

    junction_boxes = [tuple(int(rr.strip()) for rr in r.split(",")) for r in rows]

    # Initially, every junction box forms its own circuit.
    circuits = {jb: {jb} for jb in junction_boxes}

    # Compute and sort all pairwise distances.
    distances = sorted(
        (math.dist(p, q), p, q) for p, q in combinations(junction_boxes, 2)
    )

    # Merge circuits using the shortest connections.
    for _, p, q in distances[:n_connections]:
        new_circuit = circuits[p] | circuits[q]
        for pp in new_circuit:
            circuits[pp] = new_circuit

    # Find the three largest circuits.
    top_3_circuits = TopKSets(k=3)
    for s in circuits.values():
        top_3_circuits.consider(s)

    return math.prod(len(t) for t in top_3_circuits.top())


class DisjointSetUnion:
    """Disjoint Set Union (Union-Find) data structure.

    This structure maintains a collection of *disjoint sets* over `n` elements
    and supports two fundamental operations efficiently:

    - ``find(x)``:
        Returns a *representative* (root) of the set containing element ``x``.
        Elements belong to the same set if and only if their representatives
        are equal.

    - ``union(a, b)``:
        Merges the sets containing elements ``a`` and ``b``.

    Internal representation
    -----------------------
    The DSU is implemented as a forest of rooted trees:

    - Each element initially forms a singleton set and is its own parent.
    - Each tree represents one connected component.
    - The root of a tree is the representative of the set.

    Two classic optimizations are used to achieve near-constant runtime:

    1. **Union by size**
       When merging two sets, the smaller tree is attached under the larger one.
       This keeps the trees shallow and prevents worst-case degeneration.

    2. **Path compression (path halving)**
       During ``find``, parent pointers are updated so that nodes point closer
       to the root. Over time, this flattens the trees dramatically.

    Example:
    ```
    >>> dsu = DisjointSetUnion(5)
    >>> print(dsu.parent)
    >>> print(dsu.size)
    [0, 1, 2, 3, 4]
    [1, 1, 1, 1, 1]

    >>> dsu.union(2,4)
    >>> print(dsu.parent)
    >>> print(dsu.size)
    [0, 1, 2, 3, 2]
    [1, 1, 2, 1, 1]

    >>> dsu.union(0,2)
    >>> print(dsu.parent)
    >>> print(dsu.size)
    [2, 1, 2, 3, 2]
    [1, 1, 3, 1, 1]
    ```

    """

    def __init__(self, n: int) -> None:
        """Initialize `n` singleton sets.

        Args:
            n: Number of elements. Elements are identified by integers
               ``0`` through ``n - 1``.
        """
        # parent[i] = parent of i (root if parent[i] == i)
        self.parent: list[int] = list(range(n))

        # size[i] = size of the set rooted at i (valid only for roots)
        self.size: list[int] = [1] * n

        self.components: int = n  # number of disjoint sets

    def find(self, x: int) -> int:
        """Return the representative (root) of the set containing ``x``.

        This method applies *path halving*:
        each visited node is updated to point to its grandparent,
        reducing the tree height and speeding up future queries.

        Args:
            x: Element whose set representative is requested.

        Returns:
            The root index representing the set containing ``x``.
        """
        parent = self.parent
        while parent[x] != x:
            parent[x] = parent[parent[x]]  # move x one level closer to the root
            x = parent[x]
        return x

    def union(self, a: int, b: int) -> None:
        """Merge the sets containing elements ``a`` and ``b``.

        If both elements already belong to the same set, this operation
        has no effect. Otherwise, the smaller set is attached to the
        larger one (union by size).

        Args:
            a: First element.
            b: Second element.
        """
        ra = self.find(a)  # root of a
        rb = self.find(b)  # root of b

        if ra == rb:
            return False  # already in the same set

        # Attach the smaller tree under the larger tree
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra

        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        self.components -= 1
        return True

    def all_joined(self) -> bool:
        """Return True if all elements belong to a single connected component."""
        return self.components == 1


def _read_points(path: str) -> list[tuple[int, int, int]]:
    """Read 3D integer points from a comma-separated input file.

    Each line of the input file is expected to contain exactly three
    comma-separated integers representing the coordinates of a point,
    for example::

        12,34,56

    Whitespace around individual values is ignored.

    Args:
        path: Path to the input file.

    Returns:
        A list of 3-tuples ``(x, y, z)``, where each tuple represents
        a point with integer coordinates.
    """
    with open(path, "r", encoding="utf-8") as f:
        return [tuple(int(x.strip()) for x in line.split(",")) for line in f]


def _iter_edges_by_distance(
    points: list[tuple[int, int, int]],
    n_connections: int | None,
) -> list[tuple[float, int, int]] | Iterable[tuple[float, int, int]]:
    """Generate point-pair edges ordered by Euclidean distance.

    This helper constructs edges between all unique pairs of points and
    associates each edge with its Euclidean distance. Depending on the
    value of ``n_connections``, it operates in one of two modes:

    - **Partial selection**:
      If ``n_connections`` is not ``None``, only the ``n_connections`` smallest
      edges are returned using a heap-based selection strategy. This avoids
      sorting the full set of pairwise distances and is more efficient when
      only a small prefix of the shortest edges is required.

    - **Full ordering**:
      If ``n_connections`` is ``None``, all pairwise edges are materialized
      and returned in strictly increasing order of distance.

    In both cases, edges are represented as ``(distance, i, j)``, where
    ``i`` and ``j`` are indices into the ``points`` list.

    Args:
        points: List of 3D points represented as integer coordinate tuples
            ``(x, y, z)``.
        n_connections: Maximum number of shortest edges to return. If
            ``None``, all edges are returned in sorted order.

    Returns:
        Either:
        - A list containing the ``n_connections`` shortest edges, or
        - A list of all edges sorted by distance, if ``n_connections`` is
          ``None``.

        Each edge is represented as a tuple ``(distance, i, j)``.
    """
    n = len(points)

    gen = (
        (math.dist(points[i], points[j]), i, j) for i, j in combinations(range(n), 2)
    )

    if n_connections is not None:
        # Only the k smallest edges (no need to sort everything).
        return heapq.nsmallest(n_connections, gen, key=lambda t: t[0])

    # All edges in sorted order (materializes and sorts all distances).
    return sorted(gen, key=lambda t: t[0])


def _top3_product_from_dsu(dsu: DisjointSetUnion) -> int:
    """Compute the product of the three largest connected components.

    This helper extracts the sizes of all connected components represented
    by the given Disjoint Set Union (DSU) instance and returns the product
    of the three largest component sizes.

    Only root nodes are considered, as component sizes are stored at roots
    in the DSU structure.

    Args:
        dsu: A populated ``DisjointSetUnion`` instance representing a set of
            connected components.

    Returns:
        The product of the sizes of the three largest connected components.
        If fewer than three components exist, the product is taken over
        all available components.
    """
    n = len(dsu.parent)
    root_sizes = [dsu.size[i] for i in range(n) if dsu.parent[i] == i]
    return math.prod(heapq.nlargest(3, root_sizes))


def day08_1(path: str = "2025/day08/input_1.txt", n_connections: int = 1000) -> int:
    """Solve Day 08, Part 1 using a Disjoint Set Union approach.

    This function reads a list of 3D points from the input file and builds
    connected components by repeatedly merging points connected by the
    shortest pairwise distances. Only the ``n_connections`` shortest edges
    are considered, which avoids sorting all pairwise distances.

    Connectivity is tracked using a Disjoint Set Union (DSU), allowing
    near-constant-time merges and efficient component size tracking.

    The final result is computed as the product of the sizes of the three
    largest connected components.

    Args:
        path: Path to the input file containing one point per line as
            comma-separated integer coordinates.
        n_connections: Number of shortest connections (edges) to process
            when forming connected components.

    Returns:
        The product of the sizes of the three largest connected components.
        If fewer than three components exist, the product is taken over
        all available components.
    """
    points = _read_points(path)
    dsu = DisjointSetUnion(len(points))

    for _, i, j in _iter_edges_by_distance(points, n_connections=n_connections):
        dsu.union(i, j)

    return _top3_product_from_dsu(dsu)


def day08_2(
    path: str = "2025/day08/input_1.txt", n_connections: int | None = None
) -> int:
    """Solve Day 08, Part 2 using incremental connectivity.

    This function processes pairwise point connections in order of increasing
    Euclidean distance and incrementally merges connected components using a
    Disjoint Set Union (DSU).

    Merging continues until either:
    - all points belong to a single connected component, or
    - a maximum of ``n_connections`` edges have been considered (if provided).

    The return value is derived from the *last successful merge* that actually
    joined two previously separate components.

    Args:
        path: Path to the input file containing one point per line as
            comma-separated integer coordinates.
        n_connections: Optional limit on the number of shortest edges to
            consider. If ``None``, edges are processed until full connectivity
            is achieved.

    Returns:
        An integer computed from the x-coordinates of the two points involved
        in the last successful merge (multiplication). If no merge occurred (e.g., fewer than
        two points), ``0`` is returned.
    """
    points = _read_points(path)
    dsu = DisjointSetUnion(len(points))

    last_i = -1
    last_j = -1

    # If n_connections is None: consider all edges until joined.
    # If provided: consider only the k smallest edges (then maybe not fully joined).
    for _, i, j in _iter_edges_by_distance(points, n_connections=n_connections):
        if dsu.union(i, j):
            last_i, last_j = i, j
            if dsu.all_joined():
                break

    if last_i == -1:
        # No merge happened (e.g., 0 or 1 point).
        return 0

    return points[last_i][0] * points[last_j][0]


if __name__ == "__main__":
    result_1 = day08_1()  # "2025/day08/example_1.txt"
    assert result_1 == 80446, f"Real: {result_1} vs. Expected: {80446}"
    print("Solution for day08.1:", result_1)

    result_2 = day08_2()  # "2025/day08/example_1.txt"
    print("Solution for day08.2:", result_2)
    assert result_2 == 51294528, f"Real: {result_2} vs. Expected: {51294528}"
