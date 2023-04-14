from typing import Any

import networkx as nx
import queue

from src.plotting import plot_graph


def dijkstra_sp(G: nx.Graph, source_node="0") -> dict[Any, list[Any]]:
    shortest_paths = {x: [] for x in G}  # key = destination node, value = list of intermediate nodes

    # очередь с приоритетом на длину пути до вершины (длина пути, вершина)
    q = queue.PriorityQueue()

    # длина пути до каждой вершины
    dist = {x: 10**9 for x in G}

    used = {x: False for x in G}
    prev = {}

    dist[source_node] = 0
    q.put((0, source_node))

    while not q.empty():
        v = q.get()[1]
        if used[v] == True: continue
        used[v] = True

        for x in G.neighbors(v):
            # оптимизируем длину пути до вершины x
            if dist[x] > dist[v] + G[v][x]['weight']:
                dist[x] = dist[v] + G[v][x]['weight']
                prev[x] = v
                q.put((dist[x], x))

    # восстанавливаем ответ
    for x in G:
        if x == source_node: continue
        t = x
        shortest_paths[x].append(x)
        while t != source_node:
            print(prev[t])
            shortest_paths[x].append(prev[t])
            t = prev[t]

    return shortest_paths


if __name__ == "__main__":
    G = nx.read_edgelist("practicum_3/homework/graph_1.edgelist", create_using=nx.Graph)
    plot_graph(G)
    shortest_paths = dijkstra_sp(G, source_node="0")
    test_node = "5"
    shortest_path_edges = [
        (shortest_paths[test_node][i], shortest_paths[test_node][i + 1])
        for i in range(len(shortest_paths[test_node]) - 1)
    ]
    plot_graph(G, highlighted_edges=shortest_path_edges)
