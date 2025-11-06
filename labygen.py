from collections.abc import Generator
from enum import Enum, auto
from random import randint, random

from grid import CellIndex, CellType, Grid


class GenerationState(Enum):
    PREPARATION = auto()
    DIGGING = auto()


def dig_wall(grid: Grid, wall: CellIndex):
    r = random()
    if r <= 0.95:
        cell_type = CellType.EMPTY
    elif 0.95 < r <= 0.99:
        cell_type = CellType.SAND
    else:
        cell_type = CellType.WATER
    grid.set_cell(*wall, cell_type)


def dfs_maze(grid: Grid) -> Generator[tuple[CellIndex, GenerationState]]:
    for row in range(grid.height):
        for col in range(grid.width):
            grid.set_cell(row, col, CellType.WALL)
            yield (row, col), GenerationState.PREPARATION

    start = randint(0, grid.height - 1), randint(0, grid.width - 1)

    visited = set([start])
    stack: list[CellIndex] = [start]

    while stack:
        current = stack.pop()

        neighbours = grid.get_neighbours2(*current)
        for n in neighbours:
            if n not in visited:
                stack.append(current)
                wall = (
                    (current[0] + n[0]) // 2,
                    (current[1] + n[1]) // 2,
                )
                dig_wall(grid, wall)
                yield wall, GenerationState.DIGGING

                dig_wall(grid, n)
                yield n, GenerationState.DIGGING
                visited.add(n)
                stack.append(n)
                break
