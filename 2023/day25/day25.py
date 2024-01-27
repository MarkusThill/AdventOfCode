# https://en.wikipedia.org/wiki/Minimum_cut
# https://en.wikipedia.org/wiki/Karger%27s_algorithm

import networkx as nx
from functools import reduce

with open('input.txt') as f:
    lines = f.readlines()
    
lines = [l.strip().split(":") for l in lines]
G = nx.from_edgelist([(l[0], n) for l in lines for n in l[1].strip().split(" ")])

min_cuts = nx.minimum_edge_cut(G)
assert len(min_cuts) == 3
G.remove_edges_from(min_cuts)
parts = list(nx.connected_components(G))

print(f"Solution: {reduce(lambda x, y: x * y, [len(p) for p in parts], 1)}")
