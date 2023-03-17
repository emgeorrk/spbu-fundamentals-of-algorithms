import queue
from typing import Any

import networkx as nx

from src.plotting import plot_graph


def visit(node: Any):
    print(f"Wow, it is {node} right here!")


def dfs_iterative(G: nx.Graph, node: Any):
    visited = {n: False for n in G}

    stack = queue.LifoQueue()
    stack.put(node)

    while not stack.empty():
        v = stack.get()
        if visited[v] == True:
            continue
        visited[v] = True
        visit(v)
        for u in G.neighbors(v):
            if visited[u] == False:
                stack.put(u)



def topological_sort(G: nx.DiGraph, node: Any):
    visited = {n: False for n in G}

    answer = []
    def dfs(t):
        visited[t] = True
        for u in G.neighbors(t):
            if (visited[u] == False): dfs(u)
        answer.append(t)
    dfs(node)
    answer = reversed(answer)
    for x in answer: print(x, end=' ')


if __name__ == "__main__":
    # Load and plot the graph
    G = nx.read_edgelist("practicum_2/homework/graph_2.edgelist", create_using=nx.Graph)
    # plot_graph(G)

    print("Iterative DFS")
    print("-" * 32)
    dfs_iterative(G, node="0")
    print()

    G = nx.read_edgelist(
        "practicum_2/homework/graph_2.edgelist", create_using=nx.DiGraph
    )
    plot_graph(G)
    print("Topological sort")
    print("-" * 32)
    topological_sort(G, node="0")
