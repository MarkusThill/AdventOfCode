import numpy as np


def day10_1():
    file1 = open('input10_1.txt', 'r')
    lines = file1.readlines()
    lines = [l.strip() for l in lines]
    lines = [l.split(" ") for l in lines]
    lines = [(1 if l[0] == 'noop' else 2, int(l[1]) if len(l) > 1 else 0) for l in lines]

    X = np.array(lines)
    X = np.vstack([np.array([0, 1]), X])

    X_sum = X.cumsum(axis=0)

    signal_strength_list = []
    for c in range(20, X_sum[:, 0].max(), 40):
        # find index smaller than this
        idx = np.where(X_sum[:, 0] < c)[0].max()
        sig_strength = c * X_sum[idx, 1]
        signal_strength_list.append(sig_strength)

    print("Solution day 10.1:", sum(signal_strength_list))

    screen = []
    row = []
    for c in range(1, 242):
        if (c-1) % 40 == 0:
            screen.append(row)
            row = []
        idx = np.where(X_sum[:, 0] < c)[0].max()
        sprite_pos = X_sum[idx, 1]
        pixel_pos = (c-1)%40
        symbol = '#' if pixel_pos >= sprite_pos - 1 and pixel_pos <= sprite_pos + 1 else "."
        row.append(symbol)
        print("".join(row))

    print("Solution day 10.2:")
    for row in screen:
        print("".join(row))


if __name__ == '__main__':
    day10_1()
