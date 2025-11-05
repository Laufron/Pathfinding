from tkinter import Canvas
from dataclasses import dataclass


from grid import Grid, Cell
from algorithms import CellDynState

MIN_PADDING = 20


@dataclass
class Vec2:
    x: float
    y: float


class GridView:
    def __init__(
        self, grid: Grid, canvas: Canvas, canvas_width: int, canvas_height: int
    ) -> None:
        self.grid = grid
        self.canvas = canvas
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.cell_size_w = int((self.canvas_width - 2 * MIN_PADDING) / self.grid.width)
        self.cell_size_h = int(
            (self.canvas_height - 2 * MIN_PADDING) / self.grid.height
        )
        self.padding_w = (self.canvas_width - self.grid.width * self.cell_size_w) / 2
        self.padding_h = (self.canvas_height - self.grid.height * self.cell_size_h) / 2
        self.rect_pids = {}

    def get_cell_index(self, x: float, y: float) -> tuple[int, int]:
        if (
            x <= self.padding_w
            or x >= self.canvas_width - self.padding_w
            or y <= self.padding_h
            or y >= self.canvas_height - self.padding_h
        ):
            return -1, -1
        row = int((y - self.padding_h) / self.cell_size_h)
        col = int((x - self.padding_w) / self.cell_size_w)
        return row, col

    def get_cell_center_in_canvas(self, row: int, col: int) -> Vec2:
        x = self.padding_w + (col + 0.5) * self.cell_size_w
        y = self.padding_h + (row + 0.5) * self.cell_size_h
        return Vec2(x, y)

    def get_cell_color(
        self, static_state: Cell, dynamic_state: CellDynState | None = None
    ):
        if static_state == Cell.BEGIN:
            return "forest green"
        if static_state == Cell.GOAL:
            return "steel blue"
        if dynamic_state:
            match dynamic_state:
                case CellDynState.PATH:
                    return "deep pink"
                case CellDynState.QUEUED:
                    return "MediumPurple4"
                case CellDynState.VISITED:
                    return "MediumPurple1"
        match static_state:
            case Cell.EMPTY:
                return "grey8"
            case Cell.WALL:
                return "gray60"

    def draw_grid_init(self):
        for row in range(self.grid.height):
            for col in range(self.grid.width):
                center = self.get_cell_center_in_canvas(row, col)
                pid = self.canvas.create_rectangle(
                    center.x - 0.5 * self.cell_size_w,
                    center.y - 0.5 * self.cell_size_h,
                    center.x + 0.5 * self.cell_size_w,
                    center.y + 0.5 * self.cell_size_h,
                    outline="white",
                    fill="grey8",
                )
                self.rect_pids[(row, col)] = pid

    def clear_dynamic_states(self):
        for row in range(self.grid.height):
            for col in range(self.grid.width):
                static_state = self.grid.get_state(row, col)
                fill = self.get_cell_color(static_state)
                self.canvas.itemconfig(self.rect_pids[(row, col)], fill=fill)

    def update_cell(
        self, row: int, col: int, dynamic_state: CellDynState | None = None
    ):
        static_state = self.grid.get_state(row, col)
        fill = self.get_cell_color(static_state, dynamic_state)
        self.canvas.itemconfig(self.rect_pids[(row, col)], fill=fill)
