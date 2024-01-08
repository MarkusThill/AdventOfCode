from functools import reduce


def eval_expression(if_elif, x, m, a, s):
    for iff, ret in if_elif[:-1]:
        if eval(iff):
            return ret
    return if_elif[-1][0]


def split(ranges, var, cmp, value):
    sel, if_, else_ = ranges[var], ranges.copy(), ranges.copy()
    if cmp == "<":
        range_if = range(sel.start, min(sel.stop, value))
        range_else = range(max(sel.start, value), sel.stop)
    else:
        range_if = range(max(sel.start, value + 1), sel.stop)
        range_else = range(sel.start, min(sel.stop, value + 1))
    if_[var] = None if range_if.start >= range_if.stop else range_if
    else_[var] = None if range_else.start >= range_else.stop else range_else
    return if_, else_


def part_1(workflows, P):
    parts = [[exp.split("=") for exp in p[1:-1].split(",")] for p in [l for l in P]]
    parts = [{k: int(v) for k, v in p} for p in parts]

    def iterate(p, wf="in"):
        while wf not in {"A", "R"}:
            wf = eval_expression(workflows[wf], p["x"], p["m"], p["a"], p["s"])
        return wf

    solution_1 = sum([sum(p.values()) for p in parts if iterate(p) == "A"])

    print(f"Solution Day 19.1: {solution_1}")


def part_2(workflows):
    ranges = {k: range(1, 4000 + 1) for k in ["x", "m", "a", "s"]}
    q, accepted = [("in", ranges)], list()

    while q:
        k, ranges = q.pop()
        if k in {"R", "A"}:
            if k == "A":
                accepted.append(ranges)
            continue
        for cond, new_task in workflows[k][:-1]:
            if ranges is None:
                break
            sp1, ranges = split(ranges, var=cond[0], cmp=cond[1], value=int(cond[2:]))
            q.append((new_task, sp1))
        else:
            q.append((workflows[k][-1][-1], ranges))

    solution_2 = [
        reduce(lambda x, y: x * y, [v.stop - v.start for v in a.values()])
        for a in accepted
    ]
    print(f"Solution Day 19.2: {sum(solution_2)}")


def day19():
    file1 = open("2023/day19/input.txt", "r")
    lines = [l.strip() for l in file1.readlines()]

    workflows = []
    for i, l in enumerate(lines):
        if len(l) == 0:
            break
        workflows.append(l)
    workflows = {
        k: [tuple(t.split(":")) for t in v.split(",")]
        for k, v in [w[:-1].split("{") for w in workflows]
    }
    part_1(workflows, lines[i + 1 :])
    part_2(workflows)


if __name__ == "__main__":
    day19()
