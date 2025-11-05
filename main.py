from enum import Enum, auto
from typing import Literal
from tkinter import Event, Tk, Canvas

from algorithms import bfs
from grid import Grid, Cell
from gridview import GridView


WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800


class ProgramState(Enum):
    INIT = auto()
    LABYRINTH_DRAWN = auto()
    BOUNDS_CHOSEN = auto()
    SIMULATION_RUNNNING = auto()
    SIMULATION_FINISHED = auto()


if __name__ == "__main__":
    root = Tk()

    canvas = Canvas(root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg="gray50")
    canvas.pack()

    grid = Grid(width=30, height=30)
    gridview = GridView(grid, canvas, WINDOW_WIDTH, WINDOW_HEIGHT)
    gridview.draw_grid_init()

    drag_value: Cell | None = None
    start: tuple[int, int] | None = None
    goal: tuple[int, int] | None = None

    animation_step: int | Literal["idle"] = 2

    # Instructions

    def get_instruction_text(state: ProgramState):
        match state:
            case ProgramState.INIT:
                return "Clic-gauche pour créer le labyrinthe"
            case ProgramState.LABYRINTH_DRAWN:
                return "Clic-droit pour choisir les points de départ (vert) et d'arrivée (bleu). Touche <R> pour les choisir aléatoirement"
            case ProgramState.BOUNDS_CHOSEN:
                return "F1 pour lancer la simulation avec BFS (Breadth-First Search)"
            case ProgramState.SIMULATION_RUNNNING:
                return "Flèche de droite pour avance rapide"
            case ProgramState.SIMULATION_FINISHED:
                return "Touche <C> pour effacer la simulation"

    program_state = ProgramState.INIT
    instructions = canvas.create_text(
        5, 5, text=get_instruction_text(program_state), anchor="nw"
    )

    def update_instructions():
        text = get_instruction_text(program_state)
        canvas.itemconfig(instructions, text=text)

    # Utils

    def clear_start_goal():
        global start, goal
        if start:
            grid.set_cell(*start, value=Cell.EMPTY)
            gridview.update_cell(*start)
            start = None
        if goal:
            grid.set_cell(*goal, value=Cell.EMPTY)
            gridview.update_cell(*goal)
            goal = None

    # Animations

    def animate_bfs(start: tuple[int, int], goal: tuple[int, int]):
        algo = bfs(grid, start, goal)

        def step():
            global program_state
            try:
                cell, dyn_state = next(algo)
                gridview.update_cell(cell[0], cell[1], dynamic_state=dyn_state)
                root.after(ms=animation_step, func=step)
            except StopIteration:
                if program_state == ProgramState.SIMULATION_RUNNNING:
                    program_state = ProgramState.SIMULATION_FINISHED
                    update_instructions()

        step()

    # Bindings

    def on_click(event):
        global drag_value, program_state
        row, col = gridview.get_cell_index(event.x, event.y)
        if (row, col) != (-1, -1):
            drag_value = grid.toggle_wall(row, col)
            gridview.update_cell(row, col)
            if program_state == ProgramState.INIT:
                program_state = ProgramState.LABYRINTH_DRAWN
                update_instructions()

    def on_right_click(event):
        row, col = gridview.get_cell_index(event.x, event.y)
        if grid.get_state(row, col) == Cell.EMPTY:
            global start, goal, program_state
            if start and goal:
                clear_start_goal()

            if start is None:
                grid.set_cell(row, col, value=Cell.BEGIN)
                start = (row, col)
                gridview.update_cell(*start)
            else:
                grid.set_cell(row, col, value=Cell.GOAL)
                goal = (row, col)
                gridview.update_cell(*goal)

            if program_state == ProgramState.LABYRINTH_DRAWN and start and goal:
                program_state = ProgramState.BOUNDS_CHOSEN
                update_instructions()

    def on_release(event):
        global drag_value
        drag_value = None

    def on_drag(event):
        if drag_value:
            row, col = gridview.get_cell_index(event.x, event.y)
            if (row, col) != (-1, -1):
                state = grid.get_state(row, col)
                if state != drag_value:
                    grid.set_cell(row, col, drag_value)
                    gridview.update_cell(row, col)

    def on_key_press(event: Event):
        if event.keysym == "r":
            global start, goal, program_state
            if start or goal:
                clear_start_goal()

            result = grid.choose_random_bounds()
            if result:
                start = result[0], result[1]
                goal = result[2], result[3]
                gridview.update_cell(*start)
                gridview.update_cell(*goal)

            if program_state == ProgramState.LABYRINTH_DRAWN and start and goal:
                program_state = ProgramState.BOUNDS_CHOSEN
                update_instructions()

        if event.keysym == "F1":
            if start and goal:
                program_state = ProgramState.SIMULATION_RUNNNING
                update_instructions()
                animate_bfs(start, goal)

        if event.keysym == "c":
            gridview.clear_dynamic_states()
            if program_state == ProgramState.SIMULATION_FINISHED:
                program_state = ProgramState.BOUNDS_CHOSEN
                update_instructions()

        if event.keysym == "Right":
            global animation_step
            animation_step = "idle"

    def on_key_release(event: Event):
        if event.keysym == "Right":
            global animation_step
            animation_step = 2

    root.bind("<Button-1>", on_click)
    root.bind("<ButtonRelease>", on_release)
    root.bind("<B1-Motion>", on_drag)
    root.bind("<Button-2>", on_right_click)
    root.bind("<Button-3>", on_right_click)

    root.bind("<KeyPress>", on_key_press)
    root.bind("<KeyRelease>", on_key_release)

    root.mainloop()
