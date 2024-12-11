import numpy as np
import re

DEBUG = False


def fold_cube(flat_cube, n=1, visited=None):
    # actually, there are only 11 different ways to flatten a cube:
    # https: // mathworld.wolfram.com / Net.html
    if visited is None:
        visited = set()
    N_SIDES = 6
    # a side is comprised of 4 points (its corners). When the cube is still flat, the z-axis is 0 for all 4 points
    cube_side = np.matrix([[0, 1, 0, 1], [0, 0, 1, 1], [0, 0, 0, 0]])

    visited.add(n)
    solution = {n: cube_side}
    if len(visited) == N_SIDES:  # did we already visit all sides?
        return solution

    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # x-y layout: right, left, down, up

    """
    n 3D we need to account for the third axis. Rotating a vector around the origin (a point) in 2D simply 
    means rotating it around the Z-axis (a line) in 3D; since we're rotating around Z-axis, 
    its coordinate should be kept constant i.e. 0° (rotation happens on the XY plane in 3D). 
    In 3D rotating around the Z-axis would be
        |cos θ   −sin θ   0| |x|   |x cos θ − y sin θ|   |x'|
        |sin θ    cos θ   0| |y| = |x sin θ + y cos θ| = |y'|
        |  0       0      1| |z|   |        z        |   |z'|
    around the Y-axis would be

        | cos θ    0   sin θ| |x|   | x cos θ + z sin θ|   |x'|
        |   0      1       0| |y| = |         y        | = |y'|
        |−sin θ    0   cos θ| |z|   |−x sin θ + z cos θ|   |z'|
    around the X-axis would be
        |1     0           0| |x|   |        x        |   |x'|
        |0   cos θ    −sin θ| |y| = |y cos θ − z sin θ| = |y'|
        |0   sin θ     cos θ| |z|   |y sin θ + z cos θ|   |z'|
    """
    # Rotation matrices
    R_r = np.matrix([[0, 0, -1], [0, 1, 0], [1, 0, 0]])
    R_l = np.matrix([[0, 0, 1], [0, 1, 0], [-1, 0, 0]])
    R_d = np.matrix([[1, 0, 0], [0, 0, 1], [0, -1, 0]])
    R_u = np.matrix([[1, 0, 0], [0, 0, -1], [0, 1, 0]])
    rot_mat = dict()
    for k, v in zip(directions, [R_r, R_l, R_d, R_u]):
        rot_mat[k] = v

    # when moving down and left, also the location vectors have to be rotated
    Rloc_r, Rloc_l, Rloc_d, Rloc_u = np.eye(3), R_l, R_d, np.eye(3)

    # location vectors
    l_r = Rloc_r @ np.matrix([1, 0, 0]).reshape(-1, 1)
    l_l = Rloc_l @ np.matrix([-1, 0, 0]).reshape(-1, 1)
    l_d = Rloc_d @ np.matrix([0, -1, 0]).reshape(-1, 1)
    l_u = Rloc_u @ np.matrix([0, 1, 0]).reshape(-1, 1)
    loc_vec = dict()
    for k, v in zip(directions, [l_r, l_l, l_d, l_u]):
        loc_vec[k] = v

    # At least one side is not visited yet...
    # Get coordinates of current side n
    n_coord = np.where(flat_cube == n)
    assert len(n_coord) == 2
    cur_y, cur_x = n_coord[0][0], n_coord[1][0]
    for d in directions:
        dx, dy = d
        y, x = cur_y + dy, cur_x + dx
        if y < 0 or x < 0:
            continue
        if y >= flat_cube.shape[0] or x >= flat_cube.shape[1]:
            continue
        new_n = flat_cube[y, x]
        if new_n == 0 or new_n in visited:
            continue

        ans = fold_cube(flat_cube, new_n, visited)
        assert type(ans) is dict, "Type: " + str(type(ans))
        # get location vector and rotation matrix
        l, v = loc_vec[d], rot_mat[d]
        for k in ans.keys():
            assert (
                ans[k].min() == 0 and ans[k].max() == 1
            )  # all elements have to be either 0 or 1
            solution[k] = l + v @ ans[k]

    return solution


def find_side_neighbor(
    folded_cube: dict, side: int, direction: str, all_directions: list
):
    assert len(folded_cube) == 6
    assert side in folded_cube
    assert direction in all_directions
    # Choose the vectors in an order so that they describe the correct direction of the elements along the specified side
    # (top to bottom, left to right)
    # If the two matching sides later are described by vectors of opposing direction, then we also have to reverse the
    # element index when moving to a new side...
    col_idx = {"south": (0, 1), "east": (3, 1), "west": (2, 0), "north": (2, 3)}

    side_vecs = folded_cube[side][:, list(col_idx[direction])]
    found = []
    for s, v in folded_cube.items():
        if s == side:
            continue
        for d in all_directions:
            s_vecs = folded_cube[s][:, list(col_idx[d])]
            match = (side_vecs == s_vecs).all()

            # still same side, but vectors got swapped (different direction of the elements). Hence, the elements on
            # the side have to be reversed when moving from one cube side to the other
            match_reversed = (side_vecs[:, ::-1] == s_vecs).all()
            assert match + match_reversed < 2, "only one match possible"
            if match or match_reversed:
                found.append((s, d, match_reversed))

    assert len(found) == 1, "a side can only have one neighboring side"
    return found[0]


def find_all_side_neighbors(folded_cube: dict):
    directions = ["south", "west", "east", "north"]
    all_neighbors = dict()
    for s in folded_cube.keys():
        for d in directions:
            neigh = find_side_neighbor(
                folded_cube, side=s, direction=d, all_directions=directions
            )
            if s not in all_neighbors:
                all_neighbors[s] = dict()
            all_neighbors[s][d] = neigh

    return all_neighbors


def check_all_neighbors(d1, d2):
    for k in d1.keys():
        for kk in d1[k].keys():
            assert d1[k][kk] == d2[k][kk]
    return True


def read_problem_input(file="input22_1.txt"):
    file1 = open(file, "r")
    lines = file1.readlines()
    lines = [l[:-1] for l in lines]
    instructions = lines[-1]
    lines = lines[:-2]

    all_lines_length = [len(l) for l in lines]
    min_line_length, max_line_length = min(all_lines_length), max(all_lines_length)
    if DEBUG:
        print("min_line_length", min_line_length, "max_line_length", max_line_length)
        print("Padding now...")

    # pad lines which are shorter than other
    lines = [l + " " * (max_line_length - len(l)) for l in lines]
    all_lines_length = [len(l) for l in lines]
    min_line_length, max_line_length = min(all_lines_length), max(all_lines_length)
    if DEBUG:
        print("min_line_length", min_line_length, "max_line_length", max_line_length)
    assert min_line_length == max_line_length

    # count all elements not equal to ""
    sum_elements = sum([len(l.strip()) for l in lines])
    side_length = int(np.sqrt(sum_elements / 6))
    if DEBUG:
        print("side length: ", side_length)
    assert 6 * side_length**2 == sum_elements, "Side length appears to be wrong"

    instructions = re.findall("\d+|\D+", instructions)
    instructions = [i if i.isalpha() else int(i) for i in instructions]
    if DEBUG:
        print("Instructions: ", instructions)
    return lines, side_length, instructions


class Node:
    directions = {
        "north": (-1, 0),
        "east": (0, 1),
        "south": (1, 0),
        "west": (0, -1),
    }

    def __init__(self, ntype, row, column):
        # self.direction_change = dict(
        #    zip(*[self.directions.keys()] * 2))  # Map old direction to new direction. default for Most cases: same
        self.direction_change = dict()
        self.row = row
        self.column = column
        self.ntype = ntype
        self.neighbors = dict()


def map_coords_to_simple_flat_cube_idx(i, j, side_length, sfc):
    idx = i // side_length
    jdx = j // side_length
    return sfc[idx, jdx]


def reverse_direction(direction):
    dirs = list(Node.directions.keys())
    mapping = dict(zip(dirs, np.roll(dirs, -2)))
    return mapping[direction]


def build_graph(
    padded_lines, part=1, all_neighbors=None, simple_flat_cube=None, side_length=None
):
    if part == 2:
        assert all_neighbors is not None
        assert simple_flat_cube is not None
        assert side_length is not None

    padded_lines = [list(l) for l in padded_lines]
    X = np.array(padded_lines)

    # build a node for each spot
    G = np.full(X.shape, None)
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            if X[i, j] != " ":
                G[i, j] = Node(X[i, j], i, j)

    # Now connect all the Nodes with each other
    directions = Node.directions
    for i in range(G.shape[0]):
        for j in range(G.shape[1]):
            if type(G[i, j]) is Node:
                n = G[i, j]
                for d in directions:
                    di, dj = directions[d]
                    i1, j1 = i + di, j + dj
                    if (
                        0 <= i1 < G.shape[0]
                        and 0 <= j1 < G.shape[1]
                        and G[i1, j1] is not None
                    ):
                        n.neighbors[d] = G[i1, j1]
                        continue
                    if part == 1:
                        # Otherwise, we have an edge case here...
                        if d == "north":
                            # find the south-most Node in this column
                            i1 = np.where(G[:, j1])[0].max()
                        elif d == "south":
                            # find the north-most Node in this column
                            i1 = np.where(G[:, j1])[0].min()
                        elif d == "west":
                            # find the east-most Node in this row
                            j1 = np.where(G[i1, :])[0].max()
                        elif d == "east":
                            # find the west-most Node in this row
                            j1 = np.where(G[i1, :])[0].min()
                        else:
                            raise NotImplementedError()
                    elif part == 2:
                        # Where are we now (on which side of the cube)?
                        side_id = map_coords_to_simple_flat_cube_idx(
                            i, j, side_length, simple_flat_cube
                        )

                        # If we go into direction d, where do we arrive on the simplified flat cube
                        side_id_new, celestial, reverse_axis = all_neighbors[side_id][d]
                        # Local indexes within the plane of a side...
                        i1_side, j1_side = i % side_length, j % side_length

                        # This is complicated: When changing to another side of the cube, the row and column indexes
                        # might change. First of all, rows will become columns and vice versa if we move from an "east"
                        # side to a "north" side (for example). Also, it could be that the elements on a side have to be
                        # reversed since the sides might be reversed during the folding process of the cube.
                        d_ns, d_ew = ["north", "south"], ["east", "west"]
                        if celestial in d_ns:
                            P = i1_side if d in d_ew else j1_side
                            j1_side = side_length - P - 1 if reverse_axis else P
                            i1_side = 0 if celestial == "north" else side_length - 1
                        elif celestial in d_ew:
                            P = j1_side if d in d_ns else i1_side
                            i1_side = side_length - P - 1 if reverse_axis else P
                            j1_side = 0 if celestial == "west" else side_length - 1
                        else:
                            raise NotImplementedError()

                        # Transform back to real indexes on flattened big cube
                        idx_simple_next = np.where(simple_flat_cube == side_id_new)
                        ii, jj = idx_simple_next[0], idx_simple_next[1]
                        assert len(ii) == 1 and len(jj) == 1
                        ii, jj = ii[0], jj[0]
                        i1 = ii * side_length + i1_side
                        j1 = jj * side_length + j1_side
                        G[i1, j1].direction_change[(i, j)] = reverse_direction(
                            celestial
                        )

                    n.neighbors[d] = G[i1, j1]

    start = np.where(X[0, :] == ".")[0].min()
    return G[0, start]


def step(node, direction):
    n_node = node.neighbors[direction]
    if n_node.ntype == "#":  # we cannot step into a wall
        return node, direction

    last_ij = node.row, node.column
    if last_ij in n_node.direction_change:
        direction = n_node.direction_change[last_ij]
    return n_node, direction


def walk_graph(n, instructions, direction="east"):
    cdm = get_change_direction_map()
    for i in instructions:
        if type(i) is int:
            for _ in range(i):
                n, direction = step(n, direction)
        else:
            assert type(i) is str
            assert len(i) == 1
            assert i in ["R", "L"]
            direction = cdm[direction][i]

    return (
        n.row + 1,
        n.column + 1,
        dict(zip(list(Node.directions.keys()), [3, 0, 1, 2]))[direction],
    )


def get_change_direction_map():
    dirs = list(Node.directions.keys())
    roll_right = np.roll(dirs, -1)
    roll_left = np.roll(dirs, +1)
    roll_left_right = list(zip(roll_left, roll_right))

    change_dir_map = dict(
        zip(dirs, [dict(zip(["L", "R"], rl)) for rl in roll_left_right])
    )
    if DEBUG:
        print(change_dir_map)
    return change_dir_map


def input_to_simple_flat_cube(padded_lines, side_length):
    padded_lines = [list(l) for l in padded_lines]
    X = np.array(padded_lines)

    simple_shape = (X.shape[0] // side_length, X.shape[1] // side_length)
    S = np.zeros(simple_shape, dtype=np.int8)  # all flattened cubes fit in this grid

    counter = 1
    for i in range(S.shape[0]):
        for j in range(S.shape[1]):
            sub = X[
                i * side_length : (i + 1) * side_length,
                j * side_length : (j + 1) * side_length,
            ]
            if not (sub == " ").all():
                S[i, j] = counter
                counter += 1

    if DEBUG:
        print(S.shape)
        print(S)
    assert (S != 0).sum() == 6
    return S


def test_cube_folding():
    cube_shape_1 = [(0, 1), (1, 1), (2, 1), (2, 0), (3, 0), (4, 0)]

    simple_flat_cube = np.zeros((5, 5), dtype=np.int8)  # y-x layout
    for i, (y, x) in enumerate(cube_shape_1):
        simple_flat_cube[y, x] = i + 1

    print(simple_flat_cube)

    # -------------------------------------------------------------------------
    ans = fold_cube(simple_flat_cube, n=1, visited=set())
    all_neigbors_1 = find_all_side_neighbors(ans)
    print(all_neigbors_1)

    expected = dict()
    expected[1] = np.matrix([[0, 1, 0, 1], [0, 0, 1, 1], [0, 0, 0, 0]])
    expected[2] = np.matrix([[0, 1, 0, 1], [0, 0, 0, 0], [1, 1, 0, 0]])
    expected[3] = np.matrix([[0, 1, 0, 1], [1, 1, 0, 0], [1, 1, 1, 1]])
    expected[4] = np.matrix([[0, 0, 0, 0], [1, 1, 0, 0], [0, 1, 0, 1]])
    expected[5] = np.matrix([[1, 1, 0, 0], [1, 1, 1, 1], [0, 1, 0, 1]])
    expected[6] = np.matrix([[1, 1, 1, 1], [0, 0, 1, 1], [0, 1, 0, 1]])

    for k, v in ans.items():
        if k in expected:
            assert (expected[k] == ans[k]).all(), "Wrong!"
    # --------------------------------------------------------------------------
    ans = fold_cube(simple_flat_cube, n=6, visited=set())
    all_neigbors_2 = find_all_side_neighbors(ans)
    check_all_neighbors(all_neigbors_1, all_neigbors_2)

    expected = dict()
    expected[1] = np.matrix([[0, 0, 0, 0], [0, 0, 1, 1], [1, 0, 1, 0]])
    expected[2] = np.matrix([[1, 1, 0, 0], [0, 0, 0, 0], [1, 0, 1, 0]])
    expected[3] = np.matrix([[1, 1, 1, 1], [1, 1, 0, 0], [1, 0, 1, 0]])
    expected[4] = np.matrix([[0, 1, 0, 1], [1, 1, 0, 0], [1, 1, 1, 1]])
    expected[5] = np.matrix([[0, 1, 0, 1], [1, 1, 1, 1], [0, 0, 1, 1]])
    expected[6] = np.matrix([[0, 1, 0, 1], [0, 0, 1, 1], [0, 0, 0, 0]])

    for k, v in ans.items():
        if k in expected:
            assert (expected[k] == ans[k]).all(), "Wrong! " + str(k)

    # --------------------------------------------------------------------------
    ans = fold_cube(simple_flat_cube, n=3, visited=set())
    all_neigbors_3 = find_all_side_neighbors(ans)
    check_all_neighbors(all_neigbors_2, all_neigbors_3)

    expected = dict()
    expected[1] = np.matrix([[0, 1, 0, 1], [1, 1, 0, 0], [1, 1, 1, 1]])
    expected[2] = np.matrix([[0, 1, 0, 1], [1, 1, 1, 1], [0, 0, 1, 1]])
    expected[3] = np.matrix([[0, 1, 0, 1], [0, 0, 1, 1], [0, 0, 0, 0]])
    expected[4] = np.matrix([[0, 0, 0, 0], [0, 0, 1, 1], [1, 0, 1, 0]])
    expected[5] = np.matrix([[1, 1, 0, 0], [0, 0, 0, 0], [1, 0, 1, 0]])
    expected[6] = np.matrix([[1, 1, 1, 1], [1, 1, 0, 0], [1, 0, 1, 0]])

    for k, v in ans.items():
        if k in expected:
            assert (expected[k] == ans[k]).all(), "Wrong! " + str(k)


if __name__ == "__main__":
    if DEBUG:
        test_cube_folding()

    padded_lines, side_length, instructions = read_problem_input()

    n = build_graph(padded_lines, part=1)
    row, column, facing = walk_graph(n, instructions)
    print("Solution day 1:", 1000 * row + 4 * column + facing)

    sfc = input_to_simple_flat_cube(padded_lines, side_length)
    fc = fold_cube(sfc, n=6)
    all_neighbors = find_all_side_neighbors(fc)

    n = build_graph(
        padded_lines,
        part=2,
        all_neighbors=all_neighbors,
        simple_flat_cube=sfc,
        side_length=side_length,
    )
    row, column, facing = walk_graph(n, instructions)
    if DEBUG:
        print("row, column, facing", row, column, facing)
    print("Solution day 2:", 1000 * row + 4 * column + facing)
