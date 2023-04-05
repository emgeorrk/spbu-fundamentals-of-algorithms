from typing import Any

import matplotlib.pyplot as plt
import networkx as nx
import queue

from src.plotting import plot_graph


def prim_mst(G: nx.Graph, start_node="0") -> set[tuple[Any, Any]]:
    mst_set = set()  # set of nodes included into MST
    rest_set = set(G.nodes())  # set of nodes not yet included into MST
    mst_edges = set()  # set of edges constituting MST

    q = queue.PriorityQueue()
    q.put((0, (start_node, start_node)))
    #   weight, (previous node (in MST), current node (not in MST))

    while not q.empty():
        c = q.get()
        print(c)
        prev_node = c[1][0]
        curr_node = c[1][1]

        if curr_node in mst_set: continue
        mst_set.add(curr_node)
        if prev_node != curr_node: mst_edges.add((prev_node, curr_node))
        
        for v in G.neighbors(curr_node):
            dist_currnode_v = G[curr_node][v]['weight']
            if v not in mst_set: q.put((dist_currnode_v, (curr_node, v)))

    return mst_edges


if __name__ == "__main__":
    G = nx.read_edgelist("practicum_3/homework/graph_1.edgelist", create_using=nx.Graph)
    plot_graph(G)
    mst_edges = prim_mst(G, start_node="0")
    plot_graph(G, highlighted_edges=list(mst_edges))
