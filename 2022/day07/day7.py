from collections import deque


class Node:
    def __init__(self, name=None, size=0):
        self.name = name
        self.size = size
        self.parent = None
        self.children = []

    def get_child(self, name):
        for c in self.children:
            if c.name == name:
                return c
        return None

    def add_child(self, node):
        node.parent = self
        self.children.append(node)

    def update_sizes(self):
        for c in self.children:
            size = c.update_sizes()
            self.size += size
        return self.size


def day7():
    N = 100000
    N_free = 30000000
    file1 = open("2022/day07/input7_1.txt", "r")
    lines = file1.readlines()
    lines = [l.strip() for l in lines]

    root_node = Node("/", size=0)
    cur_node = root_node
    cmd = None
    for l in lines[1:]:
        if l[0] == "$":  # a command
            if l.find("$ cd ..") >= 0:
                cmd = "cd .."
                cur_node = cur_node.parent
            elif l.find("$ cd") >= 0:
                cmd = "cd"
                dirr = l.split("$ cd ")[-1]
                n = cur_node.get_child(dirr)
                assert n is not None, "Child could not be found: " + dirr
                cur_node = n
            elif l.find("$ ls") >= 0:
                cmd = "ls"
        else:
            assert cmd == "ls", "command is " + cmd + ". This should not be the case"
            # split at space
            spl = l.split(" ")
            assert len(spl) == 2
            first, second = spl[0], spl[1]
            n = Node(second, 0 if first == "dir" else int(first))
            cur_node.add_child(n)

    # Compute sizes
    n = root_node
    n.update_sizes()

    solution = 0
    stack = deque()

    for c in n.children:
        stack.append(c)

    while stack:
        s = stack.pop()
        if len(s.children) > 0:  # non-empty directory
            for c in s.children:
                stack.append(c)
            if s.size <= N:
                solution += s.size

    print("Solution day 7.1:", solution)

    n_required = N_free - (70000000 - n.size)
    assert n_required > 0
    stack = deque()
    for c in n.children:
        stack.append(c)
    solution = None
    while stack:
        s = stack.pop()
        if len(s.children) > 0:  # non-empty directory
            for c in s.children:
                stack.append(c)
            if s.size >= n_required:
                if solution is None or s.size < solution.size:
                    solution = s

    print("Solution day 7.2:", solution.size)


if __name__ == "__main__":
    day7()
