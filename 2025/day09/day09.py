from __future__ import annotations

from itertools import combinations
import time


def day09_1(
    path: str = "2025/day09/input_1.txt",
) -> int:
    """Solve Day 09, Part 1.

    Reads a list of 2D integer lattice points from the given input file and
    computes the maximum axis-aligned rectangular area that can be formed by
    choosing any two points as opposite corners.

    The area is computed on a discrete grid and includes both boundary points,
    i.e., for two points ``(x1, y1)`` and ``(x2, y2)`` the area is defined as::

        (|x1 - x2| + 1) * (|y1 - y2| + 1)

    All unordered pairs of points are considered, and the maximum such area
    is returned.

    Args:
        path: Path to the input file. Each line must contain a single point
            encoded as ``"x,y"`` with integer coordinates.

    Returns:
        The maximum inclusive area of an axis-aligned rectangle defined by
        any two points from the input.
    """
    with open(path, "r", encoding="utf-8") as f:
        points = [tuple(int(x.strip()) for x in line.split(",")) for line in f]

    all_point_pairs = combinations(points, 2)

    max_area = 0
    for p1, p2 in all_point_pairs:
        area = (abs(p1[0] - p2[0]) + 1) * (abs(p1[1] - p2[1]) + 1)
        max_area = max(area, max_area)

    return max_area


def _on_boundary(cell: tuple[int, int], poly: list[tuple[int, int]]) -> bool:
    """Check whether a point lies on the boundary of an axis-aligned polygon.

    The polygon is assumed to be *wrapped*, meaning the last vertex in ``poly``
    is implicitly connected to the first vertex. All polygon edges must be
    axis-aligned (horizontal or vertical).

    The function tests whether the given point coincides with any polygon edge,
    including endpoints.

    Args:
        cell: The point to test, given as an ``(x, y)`` integer tuple.
        poly: A list of polygon vertices ``[(x0, y0), (x1, y1), ...]`` defining
            an axis-aligned polygon. The first vertex must not be repeated at
            the end of the list.

    Returns:
        ``True`` if the point lies on any polygon edge (including endpoints),
        ``False`` otherwise.

    Raises:
        ValueError: If the polygon contains a non-axis-aligned edge.
    """
    n = len(poly)
    cx, cy = cell

    # Iterate over all polygon edges (with implicit wrap-around)
    for k in range(len(poly)):
        x1, y1 = poly[k]
        x2, y2 = poly[(k + 1) % n]

        # Check for a vertical polygon edge (x constant)
        if x1 == x2:
            # Point lies on the vertical line segment if x matches and
            # y lies within the edge's inclusive y-range
            if cx == x1 and min(y1, y2) <= cy <= max(y1, y2):
                return True

        # Check for a horizontal polygon edge (y constant)
        elif y1 == y2:
            # Point lies on the horizontal line segment if y matches and
            # x lies within the edge's inclusive x-range
            if cy == y1 and min(x1, x2) <= cx <= max(x1, x2):
                return True

        # Any other edge orientation is invalid for this function
        else:
            raise ValueError("Polygon has a non-axis-aligned edge.")

    # No boundary edge matched
    return False


def cell_inside_polygon(
    cell: tuple[int, int],
    poly: list[tuple[int, int]],
    include_boundary: bool = True,
) -> bool:
    """Check whether a grid cell is inside an axis-aligned polygon.

    The test is performed using the *cell-center rule*: the polygon is evaluated
    against the center point of the given cell. To avoid floating-point
    arithmetic, the grid is conceptually scaled by a factor of two, so that
    cell centers lie on odd integer coordinates.

    A horizontal ray is emitted to the right from the scaled cell center, and
    the number of intersections with vertical polygon edges is counted using
    the even-odd rule:
        - an even number of crossings indicates the point is outside,
        - an odd number of crossings indicates the point is inside.

    The polygon is assumed to be *wrapped*, meaning the last vertex in ``poly``
    is implicitly connected to the first vertex. All polygon edges must be
    axis-aligned (horizontal or vertical).

    Args:
        cell: The grid cell to test, given by its integer coordinates
            ``(x, y)``. The cell center is interpreted as
            ``(x + 0.5, y + 0.5)``.
        poly: A list of polygon vertices ``[(x0, y0), (x1, y1), ...]`` defining
            an axis-aligned polygon. The first vertex must not be repeated at
            the end of the list.
        include_boundary: If ``True``, a cell whose center lies exactly on the
            polygon boundary is considered inside.

    Returns:
        ``True`` if the cell center lies inside the polygon (or on its boundary
        when ``include_boundary`` is ``True``), ``False`` otherwise.

    Raises:
        ValueError: If the polygon contains a non-axis-aligned edge.
    """
    # If boundary points are considered inside, explicitly check for that first
    if include_boundary and _on_boundary(cell=cell, poly=poly):
        return True

    n = len(poly)

    # Compute the cell center in doubled coordinates (avoids floats):
    # (x + 0.5, y + 0.5) -> (2*x + 1, 2*y + 1)
    cx, cy = 2 * cell[0] + 1, 2 * cell[1] + 1

    is_inside = False

    # Iterate over all polygon edges (with implicit wrap-around)
    for k in range(len(poly)):
        x1, y1 = poly[k]
        x2, y2 = poly[(k + 1) % n]

        # Only vertical edges can intersect the horizontal ray
        if x1 == x2:  # vertical edge
            # Scale edge coordinates to doubled grid
            x = 2 * x1
            y1, y2 = 2 * y1, 2 * y2

            # Check if the ray from the cell center crosses this edge
            if cx < x and min(y1, y2) < cy < max(y1, y2):
                # Toggle inside/outside state for each crossing
                is_inside = not is_inside

        # Any non-horizontal, non-vertical edge is invalid
        elif y1 != y2:
            raise ValueError("Polygon has a non-axis-aligned edge.")

    return is_inside


def line_crosses_poly(
    line: tuple[tuple[int, int], tuple[int, int]],
    poly: list[tuple[int, int]],
) -> bool:
    """Check whether an axis-aligned line properly crosses a polygon boundary.

    The function tests for *proper* (strict interior) intersections between the
    given line segment and the boundary of an axis-aligned polygon. A proper
    crossing means that the intersection point lies strictly inside both the
    line segment and the polygon edge; touching at endpoints or overlapping
    collinearly with a polygon edge is **not** considered a crossing.

    The polygon is assumed to be *wrapped*, i.e., the last vertex in ``poly`` is
    implicitly connected to the first vertex. All polygon edges must be either
    horizontal or vertical.

    Args:
        line: The line segment to test, given by its two endpoints
            ``((x1, y1), (x2, y2))``. The line must be axis-aligned.
        poly: A list of polygon vertices ``[(x0, y0), (x1, y1), ...]`` defining
            an axis-aligned polygon. The first vertex must not be repeated at
            the end of the list.

    Returns:
        ``True`` if the line segment has a proper crossing with any polygon
        edge, ``False`` otherwise.

    Raises:
        ValueError: If the line or the polygon contains a non-axis-aligned edge.
    """
    (a1, b1), (a2, b2) = line

    # Determine line orientation: vertical if x is constant, otherwise horizontal
    v = a1 == a2
    if not (v or b1 == b2):
        raise ValueError("Line has a non-axis-aligned edge.")

    # Normalize the variable coordinate range of the line
    lo, hi = sorted((b1, b2)) if v else sorted((a1, a2))

    # Fixed coordinate of the line:
    #   - x for vertical lines
    #   - y for horizontal lines
    c = a1 if v else b1

    n = len(poly)

    # Iterate over all polygon edges with implicit wrap-around
    for (x1, y1), (x2, y2) in ((poly[i], poly[(i + 1) % n]) for i in range(n)):
        # Validate that the polygon edge is axis-aligned
        if x1 != x2 and y1 != y2:
            raise ValueError("Polygon has a non-axis-aligned edge.")

        # Only perpendicular edges can produce a proper intersection
        if (v and y1 == y2) or ((not v) and x1 == x2):
            # p: fixed coordinate of the polygon edge
            # q: variable coordinate interval of the polygon edge
            p, q = (y1, sorted((x1, x2))) if v else (x1, sorted((y1, y2)))

            # Check for strict interior–interior intersection
            if lo < p < hi and q[0] < c < q[1]:
                return True

    return False


def day09_2(
    path: str = "2025/day09/input_1.txt",
) -> int:
    """Solve Day 09, Part 2.

    Reads a set of integer lattice points that define a (not necessarily convex)
    axis-aligned polygon and computes the maximum area of an axis-aligned
    rectangle that lies completely inside the polygon.

    Unlike Part 1, the polygon may be concave. Therefore, it is not sufficient
    to consider only the rectangle corners: in addition to checking that all
    four rectangle corners lie inside the polygon, this function also verifies
    that none of the rectangle edges cross the polygon boundary at any point.

    The rectangle area is computed on a discrete grid and includes boundary
    points. For two opposite rectangle corners ``(x1, y1)`` and ``(x2, y2)``,
    the area is defined as::

        (|x1 - x2| + 1) * (|y1 - y2| + 1)

    Args:
        path: Path to the input file. Each line must contain a single point
            encoded as ``"x,y"`` with integer coordinates. The set of points is
            interpreted as the vertices of a wrapped, axis-aligned polygon.

    Returns:
        The maximum inclusive area of any axis-aligned rectangle that is fully
        contained within the polygon.
    """
    with open(path, "r", encoding="utf-8") as f:
        # Read polygon vertices from file
        points = [tuple(int(x.strip()) for x in line.split(",")) for line in f]

    # Generate all unordered pairs of polygon vertices
    all_point_pairs = combinations(points, 2)

    max_area = 0
    for p1, p2 in all_point_pairs:
        # Compute the inclusive area of the rectangle defined by p1 and p2
        area = (abs(p1[0] - p2[0]) + 1) * (abs(p1[1] - p2[1]) + 1)

        # Skip early if this rectangle cannot improve the current maximum
        if area <= max_area:
            continue

        # p1 and p2 are polygon vertices and therefore lie inside the polygon
        # Construct the remaining two rectangle corners
        p3 = (p1[0], p2[1])
        p4 = (p2[0], p1[1])

        # Ensure that all four rectangle corners lie inside the polygon
        if cell_inside_polygon(p3, points) and cell_inside_polygon(p4, points):
            # Define the four rectangle edges as line segments
            rect_lines = [(p1, p4), (p3, p2), (p1, p3), (p4, p2)]

            # Reject the rectangle if any edge crosses the polygon boundary
            if any(line_crosses_poly(line=line, poly=points) for line in rect_lines):
                continue

            # Update the maximum area found so far
            max_area = max(area, max_area)

    return max_area


if __name__ == "__main__":
    result_1 = day09_1()  # "2025/day09/example_1.txt"
    assert result_1 == 4754955192, f"Real: {result_1} vs. Expected: {4754955192}"
    print("Solution for day09.1:", result_1)

    start = time.time()
    result_2 = day09_2()  # "2025/day09/example_1.txt"
    assert result_2 == 1568849600, f"Real: {result_2} vs. Expected: {1568849600}"
    end = time.time()
