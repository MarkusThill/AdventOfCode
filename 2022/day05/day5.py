import numpy as np


def day5_1():
    # Using readlines()
    file1 = open('input5_1.txt', 'r')
    lines = file1.readlines()
    n = 4
    chunks = []
    for l in lines:
        if l.find("[") >= 0:
            chunks.append([l[i:i + n] for i in range(0, len(l), n)])

    stack = [[s.strip().replace("[", "").replace("]", "") for s in c] for c in chunks]

    # read line with stack numbering
    nums = lines[len(stack)].strip()
    num_stacks = int(nums[-1])

    # Now fill up rows of stack with empty entries
    for s in stack:
        s += [""] * (num_stacks - len(s))

    instructions = lines[len(stack)+2:]
    instructions = [i.strip() for i in instructions]
    instructions = [i.split(" ") for i in instructions]
    instructions = [ (int(i[1]), int(i[3])-1, int(i[5])-1) for i in instructions]

    # now create stack columns vectors
    stack = np.array(stack)
    stack_vecs = []
    for i in range(stack.shape[1]):
        s = stack[:, i].tolist()[::-1]
        idx = len(s)
        if '' in s:
            idx = s.index('')
        stack_vecs.append(s[:idx])

    # Now iterate through instructions
    for count, dest, target in instructions:
        ll = list(stack_vecs[dest][-count:])
        stack_vecs[dest] = list(stack_vecs[dest][:-count])
        assert len(ll) == count
        stack_vecs[target] += ll[::-1]
        #print(stack_vecs)
        #print()

    print(stack_vecs)
    print()

    solution = ""
    for s in stack_vecs:
        solution += s[-1]
    print("Solution day 5.1:", solution)


def day5_2():
    # Using readlines()
    file1 = open('input5_1.txt', 'r')
    lines = file1.readlines()
    n = 4
    chunks = []
    for l in lines:
        if l.find("[") >= 0:
            chunks.append([l[i:i + n] for i in range(0, len(l), n)])

    stack = [[s.strip().replace("[", "").replace("]", "") for s in c] for c in chunks]

    # read line with stack numbering
    nums = lines[len(stack)].strip()
    num_stacks = int(nums[-1])

    # Now fill up rows of stack with empty entries
    for s in stack:
        s += [""] * (num_stacks - len(s))

    instructions = lines[len(stack)+2:]
    instructions = [i.strip() for i in instructions]
    instructions = [i.split(" ") for i in instructions]
    instructions = [ (int(i[1]), int(i[3])-1, int(i[5])-1) for i in instructions]

    # now create stack columns vectors
    stack = np.array(stack)
    stack_vecs = []
    for i in range(stack.shape[1]):
        s = stack[:, i].tolist()[::-1]
        idx = len(s)
        if '' in s:
            idx = s.index('')
        stack_vecs.append(s[:idx])

    # Now iterate through instructions
    for count, dest, target in instructions:
        ll = list(stack_vecs[dest][-count:])
        stack_vecs[dest] = list(stack_vecs[dest][:-count])
        assert len(ll) == count
        stack_vecs[target] += ll
        #print(stack_vecs)
        #print()

    print(stack_vecs)
    print()

    solution = ""
    for s in stack_vecs:
        solution += s[-1]
    print("Solution day 5.2:", solution)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    day5_2()
