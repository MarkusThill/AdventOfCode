from z3 import Real, Solver


def day24():
    boundary = (200000000000000, 400000000000000)
    file1 = open("2023/day24/input.txt", "r")
    lines = [l.strip() for l in file1.readlines()]
    lines = [(l.split(", "), r.split(", ")) for l, r in [l.split(" @ ") for l in lines]]
    lines = [tuple(map(int, l)) for l in [(x + y) for (x, y) in lines]]

    solution_1 = 0
    for i in range(len(lines)):
        for j in range(i + 1, len(lines)):
            (a_1, b_1, _, x_1, y_1, _), (a_2, b_2, _, x_2, y_2, _) = lines[i], lines[j]
            den = x_1 * y_2 - x_2 * y_1
            if den == 0:  # parallel lines
                continue

            t_1 = ((a_2 - a_1) * y_2 + b_1 * x_2 - b_2 * x_2) / den
            t_2 = ((a_2 - a_1) * y_1 + b_1 * x_1 - b_2 * x_1) / den
            if t_1 < 0 or t_2 < 0:
                continue

            x = (-a_1 * x_2 * y_1 + x_1 * (-b_2 * x_2 + a_2 * y_2 + b_1 * x_2)) / den
            y = (-b_2 * x_2 * y_1 + y_2 * (-a_1 * y_1 + a_2 * y_1 + b_1 * x_1)) / den

            if boundary[0] <= x <= boundary[1] and boundary[0] <= y <= boundary[1]:
                solution_1 += 1

    print(f"Solution Day 24.1: {solution_1}")

    solver = Solver()
    x, y, z = Real("x"), Real("y"), Real("z")  # Our rock: start
    v_x, v_y, v_z = Real("v_x"), Real("v_y"), Real("v_z")  # Our rock: velocity

    for i, line in enumerate(lines[:3]):
        # With 3 lines, we have 9 unknowns: position(3), velocity (3), times_crossing (3)
        # And we also have 9 equations. So not more is needed
        (x_i, y_i, z_i, v_ix, v_iy, v_iz), t_i0 = line, Real(f"t_{i}")
        solver.add(x + v_x * t_i0 == x_i + v_ix * t_i0)
        solver.add(y + v_y * t_i0 == y_i + v_iy * t_i0)
        solver.add(z + v_z * t_i0 == z_i + v_iz * t_i0)

    solver.check()
    print(f"Solution Day 24.2: {solver.model().eval(x + y + z)}")


if __name__ == "__main__":
    day24()
