import numpy as np


def day18_1():
    file1 = open("input18_1.txt", "r")
    lines = file1.readlines()
    lines = [l.strip() for l in lines]
    lines = [l.split(",") for l in lines]
    lines = [[int(q) for q in l] for l in lines]

    X = np.zeros((30, 30, 30), dtype=np.int64)

    for l in lines:
        x, y, z = tuple(l)
        X[x + 1, y + 1, z + 1] = (
            1  # Otherwise we would not find those surfaces located at 0
        )

    print(
        "Solution day 18.1",
        np.abs(np.diff(X, axis=-1)).sum()
        + np.abs(np.diff(X, axis=-2)).sum()
        + np.abs(np.diff(X, axis=0)).sum(),
    )


def day18_2():
    file1 = open("input18_1.txt", "r")
    lines = file1.readlines()
    lines = [l.strip() for l in lines]
    lines = [l.split(",") for l in lines]
    lines = [[int(q) for q in l] for l in lines]

    N = np.array(lines).max() + 3
    X = np.zeros((N, N, N), dtype=np.int64)

    for l in lines:
        x, y, z = tuple(l)
        X[x + 1, y + 1, z + 1] = (
            1  # Otherwise we would not find those surfaces located at 0
        )

    # Sort of a BFS flood-fill algo..
    do_set = set()
    do_set.add((0, 0, 0))  # This point is known to be outside the droplet...
    done_set = set()
    while len(do_set) > 0:
        new_do_set = set()
        for p in do_set:
            assert X[p] == 0
            assert type(p) is tuple
            # Starting from this point, march in all directions and collect all connected points
            idx = np.array(list(p))
            for ax in range(3):
                offset = np.zeros(3, np.int8)
                for direction in [+1, -1]:
                    while True:
                        offset[ax] += direction
                        new_idx = idx + offset
                        if (new_idx < 0).any() or (new_idx >= N).any():
                            break
                        new_idx = tuple(new_idx)
                        if X[new_idx] == 1:
                            break
                        elif X[new_idx] == 0:
                            if new_idx not in done_set and new_idx not in do_set:
                                new_do_set.add(new_idx)
                        else:
                            raise NotImplementedError
            done_set.add(p)
        do_set = new_do_set

    print(len(done_set), N * N * N - X.sum())

    Q = np.zeros((N, N, N), dtype=np.int8)
    for i in done_set:
        Q[i] = 1
    Q = 1 - Q  # Invert..
    surface_total = (
        np.abs(np.diff(Q, axis=0)).sum()
        + np.abs(np.diff(Q, axis=1)).sum()
        + np.abs(np.diff(Q, axis=2)).sum()
    )

    print(surface_total, N * N * N)


if __name__ == "__main__":
    day18_2()
