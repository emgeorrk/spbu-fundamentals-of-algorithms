# Solve a maze by FIFO-based BFS.

import queue
from time import perf_counter


Maze = list[list[str]]


def read_maze(filename: str) -> Maze:
    maze = []
    with open(filename, "r") as f:
        for l in f.readlines():
            maze.append(list(l.strip()))
    return maze


def print_maze(maze: Maze, path="") -> None:
    # Find the start coordinate
    # NOTE: this bit repeat in is_valid(), make a function for that
    start_j = None
    for j, sym in enumerate(maze[0]):
        if sym == "O":
            start_j = j
            break  # NOTE: which case is handled when break is added here?
    # Find the path coordinates
    i = 0  # in the (i, j) pair, i is usually reserved for rows and j is reserved for columns
    j = start_j
    path_coords = set()
    for move in path:
        if move == "L":
            j -= 1
        elif move == "R":
            j += 1
        elif move == "U":
            i -= 1
        elif move == "D":
            i += 1
        path_coords.add((i, j))
    # Print maze + path
    for i, row in enumerate(maze):
        for j, sym in enumerate(row):
            if (i, j) in path_coords:
                print("+ ", end="")  # NOTE: end is used to avoid linebreaking
            else:
                print(f"{sym} ", end="")
        print()  # linebreak


def is_valid(maze: Maze, moves: str) -> bool:
    # Find the start coordinate
    # NOTE: this bit repeat in valid(), make a function for that
    # NOTE: is_valid() will be called in a loop. Is it necessary to compute this bit every time?
    start_j = None
    for j, sym in enumerate(maze[0]):
        if sym == "O":
            start_j = j
            break  # NOTE: which case is handled when break is added here?
    # Check each move validity
    # NOTE: this bit repeats in print_maze(). The difference in the last lines
    i = 0
    j = start_j
    for move in moves:
        if move == "L":
            j -= 1
        elif move == "R":
            j += 1
        elif move == "U":
            i -= 1
        elif move == "D":
            i += 1
        if not (0 <= i < len(maze)) or not (
            0 <= j < len(maze[0])
        ):  # row or column overflows
            return False
        elif maze[i][j] == "#":  # row/column is valid, but we hit the wall
            return False
    return True


def is_end(maze: Maze, moves: str) -> bool:
    # Find the start coordinate
    # NOTE: this bit repeat in valid(), make a function for that
    # NOTE: is_end() will be called in a loop. Is it necessary to compute this bit every time?
    start_j = None
    for j, sym in enumerate(maze[0]):
        if sym == "O":
            start_j = j
            break  # NOTE: which case is handled when break is added here?
    # Going until the end
    i = 0
    j = start_j
    for move in moves:
        if move == "L":
            j -= 1
        elif move == "R":
            j += 1
        elif move == "U":
            i -= 1
        elif move == "D":
            i += 1
    # Check the end
    if maze[i][j] == "X":
        print(f"Found: {moves}")
        print_maze(maze, moves)
        return True
    return False


def solve(maze: Maze):
    # FIFO-based BFS
    q = queue.Queue()  # it is a FIFO queue
    path = ""
    q.put(path)
    while not is_end(maze, path):
        path = q.get()
        for move in ["L", "R", "U", "D"]:
            new_path = path + move
            if is_valid(maze, new_path):
                q.put(new_path)


if __name__ == "__main__":
    maze = read_maze("practicum_2/maze_2.txt")
    t_start = perf_counter()
    solve(maze)
    t_end = perf_counter()
    print(f"Elapsed time: {t_end - t_start} sec")
