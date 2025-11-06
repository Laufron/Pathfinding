import random
from enum import Enum, auto

CellIndex = tuple[int, int]


class CellType(Enum):
    EMPTY = auto()
    SAND = auto()
    WATER = auto()
    WALL = auto()
    BEGIN = auto()
    GOAL = auto()


class Grid:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.cells: list[list[CellType]] = [
            [CellType.EMPTY for _ in range(width)] for _ in range(height)
        ]

    def get_cell_type(self, row: int, col: int):
        return self.cells[row][col]

    def set_cell(self, row: int, col: int, value: CellType):
        self.cells[row][col] = value

    def reset(self):
        for row in range(self.height):
            for col in range(self.width):
                self.set_cell(row, col, CellType.EMPTY)

    def get_cell_cost(self, row: int, col: int) -> float:
        state = self.get_cell_type(row, col)
        match state:
            case CellType.EMPTY:
                return 1
            case CellType.SAND:
                return 2
            case CellType.WATER:
                return 5
            case CellType.BEGIN:
                return 1
            case CellType.GOAL:
                return 1
            case CellType.WALL:
                return float("inf")

    def get_neighbours(self, row: int, col: int) -> list[CellIndex]:
        neighbours = []
        positions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for position in positions:
            new_row = row + position[0]
            new_col = col + position[1]
            if 0 <= new_row < self.height and 0 <= new_col < self.width:
                neighbours.append((new_row, new_col))
        random.shuffle(neighbours)
        return neighbours

    def toggle_cell_type(self, row: int, col: int, cell_type: CellType) -> CellType:
        if self.cells[row][col] == cell_type:
            value = CellType.EMPTY
        else:
            value = cell_type
        self.cells[row][col] = value
        return value

    def choose_random_bounds(self) -> tuple[CellIndex, CellIndex] | None:
        candidates = []
        for row in range(self.height):
            for col in range(self.width):
                if self.cells[row][col] != CellType.WALL:
                    candidates.append((row, col))
        if candidates:
            start, end = random.choices(candidates, k=2)
            self.set_cell(*start, value=CellType.BEGIN)
            self.set_cell(*end, value=CellType.GOAL)
            return start, end
        return None
