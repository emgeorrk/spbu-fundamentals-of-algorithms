# Improvements:
# 1. Moving most of the function to Class Maze (no perf drop)
# 2. Moving if-elif chains to a separate function (perf drop from 0.8s to 1.2s)
# 3. Simple heuristic: do not cancel the last move, e.g., do not go L if the last move is R (perf up to 0.004s)

import queue
from time import perf_counter


class Maze:
    def __init__(self, list_view: list[list[str]]):
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

    def is_valid(self, moves: str) -> bool:
        i = 0
        j = self.start_j
        for move in moves:
            i, j = _shift_coordinate(i, j, move)
            if not (0 <= i < len(self.list_view)) or not (
                0 <= j < len(self.list_view[0])
            ):  # row or column overflows
                return False
            elif (
                self.list_view[i][j] == "#"
            ):  # row/column is valid, but we hit the wall
                return False
        return True

    def is_end(self, moves: str) -> bool:
        # Going until the end
        i = 0
        j = self.start_j
        for move in moves:
            i, j = _shift_coordinate(i, j, move)
        # Check the end
        return self.list_view[i][j] == "X"

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


def solve(maze: Maze):
    # FIFO-based BFS
    q = queue.Queue()  # it is a FIFO queue
    path = ""
    q.put(path)
    while not maze.is_end(path):
        path = q.get()
        # for move in ["L", "R", "U", "D"]:  # NOTE: previous version
        for move in _possible_moves(path):
            new_path = path + move
            if maze.is_valid(new_path):
                q.put(new_path)
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


def _possible_moves(path: str) -> list[str]:
    moves = ["L", "R", "U", "D"]
    if not path:
        return moves
    last_move = path[-1]
    if last_move == "L":
        moves.remove("R")
    elif last_move == "R":
        moves.remove("L")
    elif last_move == "U":
        moves.remove("D")
    elif last_move == "D":
        moves.remove("U")
    return moves


if __name__ == "__main__":
    maze = Maze.from_file("practicum_2/maze_2.txt")
    t_start = perf_counter()
    solve(maze)
    t_end = perf_counter()
    print(f"Elapsed time: {t_end - t_start} sec")
