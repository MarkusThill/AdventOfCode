def eval_expression(if_else, x, m, a, s):
    for iff, ret in if_else[:-1]:
        if eval(iff):
            return ret
    return if_else[-1][0]


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
    parts = [
        [exp.split("=") for exp in p[1:-1].split(",")]
        for p in [l for l in lines[i + 1 :]]
    ]
    parts = [{k: int(v) for k, v in p} for p in parts]

    def iterate(p, wf="in"):
        while wf not in {"A", "R"}:
            wf = eval_expression(workflows[wf], p["x"], p["m"], p["a"], p["s"])
        return wf

    solution_1 = sum([sum(p.values()) for p in parts if iterate(p) == "A"])

    print(f"Solution Day 19.1: {solution_1}")


if __name__ == "__main__":
    day19()
