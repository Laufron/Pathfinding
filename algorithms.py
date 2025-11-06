import math
from collections import deque
from collections.abc import Generator
from enum import Enum, auto
from heapq import heappop, heappush
from itertools import count

from grid import CellIndex, CellType, Grid


class CellDynState(Enum):
    VISITED = auto()
    QUEUED = auto()
    PATH = auto()


def bfs(
    grid: Grid, start: CellIndex, goal: CellIndex
) -> Generator[tuple[CellIndex, CellDynState]]:
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
                cell_type = grid.get_cell_type(*neighbour)
                if cell_type != CellType.WALL:
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


def dijkstra(
    grid: Grid, start: CellIndex, goal: CellIndex
) -> Generator[tuple[CellIndex, CellDynState]]:
    counter = count()
    min_distances: dict[CellIndex, float] = {start: 0}
    parents = dict()

    min_heap = [(min_distances[start], next(counter), start)]

    while min_heap:
        current_distance, _, current = heappop(min_heap)
        if current_distance > min_distances[current]:
            # Cas ou on a trouvé un chemin plus court vers la cellule entre temps : on ignore le chemin long
            continue

        yield current, CellDynState.VISITED

        if current == goal:
            break

        for neighbour in grid.get_neighbours(*current):
            cell_cost = grid.get_cell_cost(*neighbour)
            if math.isinf(cell_cost):
                continue

            new_neighbour_distance = min_distances[current] + cell_cost
            if (
                neighbour not in min_distances
                or new_neighbour_distance < min_distances[neighbour]
            ):
                min_distances[neighbour] = new_neighbour_distance
                parents[neighbour] = current
                heappush(min_heap, (new_neighbour_distance, next(counter), neighbour))
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


def A_star(
    grid: Grid, start: CellIndex, goal: CellIndex
) -> Generator[tuple[CellIndex, CellDynState]]:
    # g: cout reel
    # h: heuristique
    # f = g + h
    counter = count()
    min_gscore: dict[CellIndex, float] = {start: 0}
    parents = dict()

    min_heap = [(min_gscore[start] + h(start, goal), next(counter), start)]

    while min_heap:
        current_fscore, _, current = heappop(min_heap)
        if current_fscore - h(current, goal) > min_gscore[current]:
            # Cas ou on a trouvé un chemin plus court vers la cellule entre temps : on ignore le chemin long
            continue

        yield current, CellDynState.VISITED

        if current == goal:
            break

        for neighbour in grid.get_neighbours(*current):
            cell_cost = grid.get_cell_cost(*neighbour)
            if math.isinf(cell_cost):
                continue

            neighbour_gscore = min_gscore[current] + cell_cost
            if neighbour not in min_gscore or neighbour_gscore < min_gscore[neighbour]:
                min_gscore[neighbour] = neighbour_gscore
                parents[neighbour] = current
                heappush(
                    min_heap,
                    (neighbour_gscore + h(neighbour, goal), next(counter), neighbour),
                )
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


def h(cell: CellIndex, goal: CellIndex):
    # Heuristique qui estime la distance par rapport à la cible
    return abs(cell[0] - goal[0]) + abs(cell[1] - goal[1])
