import random
from enum import Enum, auto


class Cell(Enum):
    EMPTY = auto()
    WALL = auto()
    BEGIN = auto()
    GOAL = auto()


class Grid:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.cells: list[list[Cell]] = [
            [Cell.EMPTY for _ in range(width)] for _ in range(height)
        ]

    def get_state(self, row: int, col: int):
        return self.cells[row][col]

    def set_cell(self, row: int, col: int, value: Cell):
        self.cells[row][col] = value

    def toggle_wall(self, row: int, col: int) -> Cell:
        if self.cells[row][col] == Cell.WALL:
            value = Cell.EMPTY
        else:
            value = Cell.WALL
        self.cells[row][col] = value
        return value

    def choose_random_bounds(self) -> tuple[int, int, int, int] | None:
        candidates = []
        for row in range(self.height):
            for col in range(self.width):
                if self.cells[row][col] == Cell.EMPTY:
                    candidates.append((row, col))
        if candidates:
            start, end = random.choices(candidates, k=2)
            self.set_cell(*start, value=Cell.BEGIN)
            self.set_cell(*end, value=Cell.GOAL)
            return *start, *end
        return None

    def get_neighbours(self, row: int, col: int) -> list[tuple[int, int]]:
        neighbours = []
        positions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for position in positions:
            new_row = row + position[0]
            new_col = col + position[1]
            if 0 <= new_row < self.height and 0 <= new_col < self.width:
                if self.get_state(new_row, new_col) != Cell.WALL:
                    neighbours.append((new_row, new_col))
        return neighbours
