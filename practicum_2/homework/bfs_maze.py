from time import perf_counter
import queue
import networkx as nx

class Maze:
    def __init__(self, list_view: list[list[str]]) -> None:
        self.list_view = list_view
        self.start_j = None
        for j, sym in enumerate(self.list_view[0]):
            if sym == "O":
                self.start_j = j

    @classmethod
    def from_file(cls, filename):
        list_view = []
        with open(filename, "r") as f:
            for l in f.readlines():
                list_view.append(list(l.strip()))
        obj = cls(list_view)
        return obj

    def print(self, path="") -> None:
        # Find the path coordinates
        i = 0  # in the (i, j) pair, i is usually reserved for rows and j is reserved for columns
        j = self.start_j
        path_coords = set()
        for move in path:
            i, j = _shift_coordinate(i, j, move)
            path_coords.add((i, j))
        # Print maze + path
        for i, row in enumerate(self.list_view):
            for j, sym in enumerate(row):
                if (i, j) in path_coords:
                    print("+ ", end="")  # NOTE: end is used to avoid linebreaking
                else:
                    print(f"{sym} ", end="")
            print()  # linebreak


def solve(maze: Maze) -> None:
    path = ""  # solution as a string made of "L", "R", "U", "D"

    G = nx.Graph()

    for i in range(0, len(maze.list_view)):
        for j in range(0, len(maze.list_view[i])):
            if maze.list_view[i][j] == '#': continue
            if maze.list_view[i][j] == 'X': finish = (i,j)
            if i+1 < len(maze.list_view) and maze.list_view[i+1][j] != '#': G.add_edge((i,j), (i+1,j))
            if j+1 < len(maze.list_view[i]) and maze.list_view[i][j+1] != '#': G.add_edge((i,j), (i,j+1))

    dist = {}
    dist[0,maze.start_j] = 0

    q = queue.Queue()
    q.put((0,maze.start_j))

    while not q.empty():
        v = q.get()
        for u in G.neighbors(v):
            if dist.get(u) == None or dist[u] > dist[v] + 1:
                dist[u] = dist[v] + 1
                q.put(u)

    while finish != (0, maze.start_j):
        print(finish)
        for u in G.neighbors(finish):
            u_i,u_j = u
            finish_i, finish_j = finish
            if dist[u] == dist[finish] - 1:
                if finish_i - 1 == u_i and finish_j == u_j: path += 'D'
                if finish_i + 1 == u_i and finish_j == u_j: path += 'U'
                if finish_i == u_i and finish_j - 1 == u_j: path += 'R'
                if finish_i == u_i and finish_j + 1 == u_j: path += 'L'
                finish = u
                break
    path = reversed(path)

    print(f"Found: {path}")
    maze.print(path)


def _shift_coordinate(i: int, j: int, move: str) -> tuple[int, int]:
    if move == "L":
        j -= 1
    elif move == "R":
        j += 1
    elif move == "U":
        i -= 1
    elif move == "D":
        i += 1
    return i, j


if __name__ == "__main__":
    maze = Maze.from_file("practicum_2/homework/maze_2.txt")
    t_start = perf_counter()
    solve(maze)
    t_end = perf_counter()
    print(f"Elapsed time: {t_end - t_start} sec")
