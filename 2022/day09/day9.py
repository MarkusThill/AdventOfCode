import numpy as np


def update_tail(h, t):
    if (np.abs(h - t) > np.array([1, 1])).any():
        t += np.sign(h - t)
    return t  # Tail stays the same


def day9():
    file1 = open("2022/day09/input9_1.txt", "r")
    lines = file1.readlines()
    lines = [l.strip() for l in lines]
    lines = [l.split(" ") for l in lines]
    lines = [(l[0], int(l[1])) for l in lines]

    grid_size = 1000
    grid = np.zeros((grid_size, grid_size)) == 1

    H = np.array([grid_size // 2, grid_size // 2])
    tail_list = [np.array(H) for _ in range(9)]

    for inst in lines:
        d = inst[0]
        if d == "R":
            dir_vec = [0, 1]
        elif d == "L":
            dir_vec = [0, -1]
        elif d == "U":
            dir_vec = [1, 0]
        elif d == "D":
            dir_vec = [-1, 0]
        else:
            raise "Error"
        dir_vec = np.array(dir_vec)
        for _ in range(inst[1]):
            H += dir_vec
            new_H = H
            for j in range(len(tail_list)):
                T = np.array(tail_list[j])
                T = update_tail(new_H, T)
                assert (T >= 0).all(), "Grid is too small"
                # When to update tail?
                # None of the previous tails should have the update position
                cmp = (T == np.stack(tail_list))[:j].all(axis=1).any()

                if not cmp:
                    tail_list[j] = np.array(T)
                if j == len(tail_list) - 1:
                    grid[T[0], T[1]] |= True
                new_H = np.array(T)

    print("Solution day 9.1/2:", grid.sum())


if __name__ == "__main__":
    day9()
