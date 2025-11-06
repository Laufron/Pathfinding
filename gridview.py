from dataclasses import dataclass
from tkinter import Canvas

from algorithms import CellDynState
from grid import CellIndex, CellType, Grid

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
        self.rect_pids: dict[CellIndex, list[int]] = dict()
        self.dyn_states: dict[CellIndex, CellDynState] = dict()

    def get_cell_index(self, x: float, y: float) -> CellIndex:
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
        self, static_state: CellType, dynamic_state: CellDynState | None = None
    ):
        if static_state == CellType.BEGIN:
            return "lime green"
        if static_state == CellType.GOAL:
            return "DodgerBlue2"
        if dynamic_state:
            match dynamic_state:
                case CellDynState.PATH:
                    return "deep pink"
                case CellDynState.QUEUED:
                    return "MediumPurple4"
                case CellDynState.VISITED:
                    return "MediumPurple1"
        match static_state:
            case CellType.EMPTY:
                return "grey8"
            case CellType.WALL:
                return "gray60"
            case CellType.SAND:
                return "goldenrod1"
            case CellType.WATER:
                return "DeepSkyBlue2"

    def draw_grid_init(self):
        for row in range(self.grid.height):
            for col in range(self.grid.width):
                center = self.get_cell_center_in_canvas(row, col)
                pid = self.canvas.create_rectangle(
                    center.x - 0.5 * self.cell_size_w,
                    center.y - 0.5 * self.cell_size_h,
                    center.x + 0.5 * self.cell_size_w,
                    center.y + 0.5 * self.cell_size_h,
                    outline="grey30",
                    fill="grey8",
                )
                self.rect_pids[(row, col)] = [pid]

    def clear_dynamic_states(self, except_state: CellDynState | None = None):
        for cell_index, dyn_state in self.dyn_states.items():
            if dyn_state != except_state:
                rectangles = self.rect_pids[cell_index]
                if len(rectangles) == 2:
                    self.canvas.delete(rectangles.pop())

                else:
                    static_state = self.grid.get_cell_type(*cell_index)
                    fill = self.get_cell_color(static_state)
                    self.canvas.itemconfig(rectangles[0], fill=fill)

    def update_cell(
        self, row: int, col: int, dynamic_state: CellDynState | None = None
    ):
        static_state = self.grid.get_cell_type(row, col)
        fill = self.get_cell_color(static_state, dynamic_state)

        rectangles = self.rect_pids[(row, col)]
        if (
            dynamic_state == CellDynState.PATH
            and static_state != CellType.BEGIN
            and static_state != CellType.GOAL
        ):
            static_color = self.get_cell_color(static_state)
            self.canvas.itemconfig(rectangles[0], fill=static_color)
            center = self.get_cell_center_in_canvas(row, col)
            rectangles.append(
                self.canvas.create_rectangle(
                    center.x - 0.3 * self.cell_size_w,
                    center.y - 0.3 * self.cell_size_h,
                    center.x + 0.3 * self.cell_size_w,
                    center.y + 0.3 * self.cell_size_h,
                    outline="",
                    fill=fill,
                )
            )
        else:
            self.canvas.itemconfig(rectangles[0], fill=fill)
        if dynamic_state:
            self.dyn_states[(row, col)] = dynamic_state

    def update_full_grid(self):
        for row in range(self.grid.height):
            for col in range(self.grid.width):
                self.update_cell(row, col)
