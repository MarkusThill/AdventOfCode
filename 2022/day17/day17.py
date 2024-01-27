import numpy as np
from itertools import cycle


def print_board(X):
    top = get_tower_top(X)
    for i in reversed(range(top)):
        row = np.full(7, ".")
        row[X[i] >= 1] = "#"
        print("|", "".join(row.tolist()), "|", sep="")
    print()


def get_tower_top(X):
    return np.where(X.sum(axis=1) == 0)[0].min()


def apply_wind(X, s, s_x, s_y, direction):
    inc_x = 0
    if direction == ">":
        # can we blow to the right?
        if s_x + s.shape[1] < 7:
            inc_x += 1
    elif direction == "<":
        # can we blow to the left
        if s_x > 0:
            inc_x -= 1
    else:
        raise NotImplementedError()

    if not has_collision(X, s_x + inc_x, s_y, s):
        return s_x + inc_x

    return s_x


def has_collision(X, s_x, s_y, s):
    rng_x = slice(s_x, s_x + s.shape[1])
    rng_y = slice(s_y - s.shape[0], s_y)
    return ((X[rng_y, rng_x] + s) >= 2).sum() > 0


def day17_1():
    H = 6000
    N = 2022
    # Using readlines()
    file1 = open("test.txt", "r")
    lines = file1.readlines()
    lines = [l.strip() for l in lines]
    assert len(lines) == 1
    wind = cycle(list(lines[0]))

    shape1 = np.ones((1, 4))
    shape2 = np.zeros((3, 3))
    shape2[:, 1] = 1
    shape2[1, :] = 1
    shape3 = np.zeros((3, 3))
    shape3[:, 2] = 1
    shape3[2, :] = 1
    shape3 = shape3[::-1, :]

    shape4 = np.ones((4, 1))
    shape5 = np.ones((2, 2))

    shapes = cycle([shape1, shape2, shape3, shape4, shape5])

    X = np.zeros((H, 7), np.int8)
    # set bottom row to ones
    X[0, :] = 1

    print_board(X)

    cycle_set = set()
    for i in range(N):
        # get next shape
        s = next(shapes)
        # print(s)
        # get current top of tower
        top = get_tower_top(X)

        # starting point of shape (handle is top-left)
        s_y = top + 3 + s.shape[0]
        s_x = 2
        at_rest = 1
        toggle = False
        while at_rest > 0:
            if not toggle:  # alternate between blowing wind and falling
                # apply wind
                s_x = apply_wind(X, s, s_x, s_y, next(wind))
            else:
                if not has_collision(X, s_x, s_y - 1, s):
                    s_y -= 1
                else:
                    at_rest -= 1
            toggle = not toggle

        rng_x = slice(s_x, s_x + s.shape[1])
        rng_y = slice(s_y - s.shape[0], s_y)
        X[rng_y, rng_x] = s

    print("Solution day 17.1", get_tower_top(X) - 1)


def signature(X):
    return tuple(X[get_tower_top(X) - 50 : get_tower_top(X)].flatten().tolist())


def day17_2():
    H = 6000
    N = 2000
    # Using readlines()
    file1 = open("input17_1.txt", "r")
    lines = file1.readlines()
    lines = [l.strip() for l in lines]
    assert len(lines) == 1
    wind = cycle(list(lines[0]))

    shape1 = np.ones((1, 4))
    shape2 = np.zeros((3, 3))
    shape2[:, 1] = 1
    shape2[1, :] = 1
    shape3 = np.zeros((3, 3))
    shape3[:, 2] = 1
    shape3[2, :] = 1
    shape3 = shape3[::-1, :]

    shape4 = np.ones((4, 1))
    shape5 = np.ones((2, 2))

    shapes = cycle([shape1, shape2, shape3, shape4, shape5])

    X = np.zeros((H, 7), np.int8)
    # set bottom row to ones
    X[0, :] = 1

    print_board(X)

    index_tracker = dict()
    height_tracker = dict()
    for i in range(N):
        # get next shape
        s = next(shapes)
        # print(s)
        # get current top of tower
        top = get_tower_top(X)

        # starting point of shape (handle is top-left)
        s_y = top + 3 + s.shape[0]
        s_x = 2
        at_rest = 1
        toggle = False
        while at_rest > 0:
            if not toggle:  # toggle between wind and falling
                # apply wind
                old_sx = s_x
                s_x = apply_wind(s, s_x, next(wind))
                rng_y = slice(s_y - s.shape[0], s_y)
                rng_x = slice(s_x, s_x + s.shape[1])
                if ((X[rng_y, rng_x] + s) >= 2).sum() != 0:
                    s_x = old_sx  # undo move, since we had a collision
            else:
                rng_x = slice(s_x, s_x + s.shape[1])
                rng_y = slice(s_y - s.shape[0] - 1, s_y - 1)
                if ((X[rng_y, rng_x] + s) >= 2).sum() == 0:
                    s_y -= 1
                else:
                    at_rest -= 1
            toggle = not toggle
            # print(s_x, s_y)

        rng_x = slice(s_x, s_x + s.shape[1])
        rng_y = slice(s_y - s.shape[0], s_y)
        X[rng_y, rng_x] = s

        if i > 100:
            sig = (signature(X), s.shape, int(s[-1, -1]))
            if sig in index_tracker:
                print("Found cycle at:", i)
                print("Previous signature at:", index_tracker[sig])
                cycle_len = i - index_tracker[sig]["idx"]
                print("cycle:", cycle_len)
                cycle_height = (
                    get_tower_top(X) - index_tracker[sig]["height"]
                )  # off by one here...
                print("cycle-height:", cycle_height)
            index_tracker[sig] = {"idx": i, "height": get_tower_top(X) - 1}

        height_tracker[i + 1] = get_tower_top(X)  # off by one here..

    print(
        "Solution day 17.2:",
        (1_000_000_000_000 // cycle_len) * cycle_height
        + height_tracker[1_000_000_000_000 % cycle_len],
    )


if __name__ == "__main__":
    day17_1()
