from collections import deque
from enum import Enum, auto


from grid import Grid


class CellDynState(Enum):
    VISITED = auto()
    QUEUED = auto()
    PATH = auto()


def bfs(grid: Grid, start: tuple[int, int], goal: tuple[int, int]):
    queue = deque([start])
    visited = set([start])
    parents = dict()

    while queue:
        current = queue.popleft()
        yield current, CellDynState.VISITED

        if current == goal:
            break

        for neighbour in grid.get_neighbours(*current):
            if neighbour not in visited:
                visited.add(neighbour)
                parents[neighbour] = current
                queue.append(neighbour)
                yield neighbour, CellDynState.QUEUED

    if goal in parents:
        path = []
        node = goal
        while node != start:
            path.append(node)
            node = parents[node]
        path.append(start)
        path.reverse()
        for node in path:
            yield node, CellDynState.PATH
