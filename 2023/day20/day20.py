from collections import deque, OrderedDict
import math


def day20():
    file1 = open("2023/day20/input.txt", "r")
    lines = [l.strip() for l in file1.readlines()]

    modules, all_nexts = dict(), set()
    for l in lines:
        left, right = l.split(" -> ")
        op, name, nex = left[0], left if left[0] == "b" else left[1:], right.split(", ")
        m = {"op": op, "next": nex, "name": name, "in": OrderedDict(), "out": False}
        all_nexts |= set(nex)
        modules[name] = m
    assert len(all_nexts - modules.keys()) == 1
    out, lout = list(all_nexts - modules.keys())[0], set()
    modules[out] = {"op": None, "next": [], "name": out, "in": OrderedDict()}

    # Conjunction modules already need to know all their inputs, which are initialized to False
    for m in [m for m in modules.values() if m["op"] == "&"]:
        f = lambda n: [mm["name"] for mm in modules.values() if n in mm["next"]]
        for iname in f(m["name"]):
            m["in"][iname] = False  # Initialize particular input to 'low'
        lout |= set(f(out))  # Find the module which sends the signal to out='rx'
    assert len(lout) == 1

    q, counter = deque(), {False: 0, True: 0}
    final_layer_in = {m["name"] for m in modules.values() if list(lout)[0] in m["next"]}
    cycles = {k: list() for k in final_layer_in}
    for n_button in range(10**4):
        counter[False] += 1  # Pressing button also sends a low signal to 'broadcaster'
        q.appendleft("broadcaster")
        while q:
            m = modules[name := q.pop()]
            if m["op"] == "%":
                inp_val = m["in"].popitem(last=False)[-1] if len(m["in"]) > 0 else True
                if inp_val:
                    continue
                m["out"] = not m["out"]
            elif m["op"] == "&":  # Essentially, a Boolean NAND Gate
                m["out"] = not all(modules[n]["out"] for n in m["in"])

            for n in m["next"]:
                modules[n]["in"][name] = m["out"]
                q.appendleft(n)
                counter[m["out"]] += 1

            for mm in cycles.keys():
                if modules[mm]["out"] and n_button not in cycles[mm]:
                    cycles[mm].append(n_button)

        if n_button == 1000 - 1:
            print(f"Solution Day 20.1: {counter[False] * counter[True]}")

        if all(len(v) >= 2 for v in cycles.values()):
            solution_2 = math.lcm(*(v[1] - v[0] for v in cycles.values()))
            print(f"Solution Day 20.2: {solution_2}")
            return


if __name__ == "__main__":
    day20()
