from typing import Dict, Final

from textual.app import App, ComposeResult, RenderResult
from textual.containers import Container, HorizontalGroup
from textual.widget import Widget
from textual.widgets import Label

DEFAULT_GRID_DIMENSION: Final[int] = 5


class Cell(Widget, can_focus=True):
    def __init__(self, x: int, y: int, *args, **kwargs):
        self.x = x
        self.y = y
        super().__init__(*args, **kwargs)
    
    def render(self) -> RenderResult:
        return ""
    
    def on_click(self) -> None:
        self.toggle_class("painted")


class Grid(Container):
    def __init__(self, dimension: int = DEFAULT_GRID_DIMENSION):
        self.dimension: int = dimension
        super().__init__()

        self.styles.grid_size_rows = self.styles.grid_size_columns = dimension

    def compose(self) -> ComposeResult:
        backgrounds: Dict[str] = {
            True: "checkerboard-a",
            False: "checkerboard-b",
        }

        q_cells: int = self.dimension**2
        bg_type: bool = True
        for i in range(q_cells):
            x = i % self.dimension
            y = int(i / self.dimension)
            yield Cell(x, y, id=f"cell_{x}_{y}", classes=f"{backgrounds[bg_type]}")
            bg_type = not bg_type

class TopFrame(Container):
    def __init__(self, lenght: int):
        self.lenght = lenght
        super().__init__()

        self.styles.grid_size_columns = lenght

    def compose(self) -> ComposeResult:
        for _ in range(self.lenght):
            yield Label(f"{_}\n{_}\n{_}")


class LeftFrame(Container):
    def __init__(self, lenght: int):
        self.lenght = lenght
        super().__init__()

        self.styles.grid_size_rows = lenght

    def compose(self) -> ComposeResult:
        for _ in range(self.lenght):
            yield Label(f"{_} {_}")


class Board(Container):
    def compose(self) -> ComposeResult:
        yield TopFrame(5)
        yield HorizontalGroup(LeftFrame(5), Grid(5))


class PycrossApp(App):
    CSS_PATH = "pycross.tcss"
    BINDINGS = [
        ("up", "traverse_grid(0,-1)", "Move Up"),
        ("down", "traverse_grid(0,1)", "Move Down"),
        ("left", "traverse_grid(-1,0)", "Move Left"),
        ("right", "traverse_grid(1,0)", "Move Right"),
        ("z", "paint_tile", "Paint Tile"),
    ]

    def compose(self) -> ComposeResult:
        yield Board()

    def action_traverse_grid(self, x_direction: int, y_direction: int) -> None:
        grid: Grid = self.query_exactly_one(Grid)
        current_cell: Cell = self.focused

        next_x: int = current_cell.x + x_direction
        next_y: int = current_cell.y + y_direction

        if next_x >= 0 and next_x < grid.dimension and next_y >= 0 and next_y < grid.dimension:
            next_cell: Cell = self.query_exactly_one(f"#cell_{next_x}_{next_y}")
            self.set_focus(next_cell)
    
    def action_paint_tile(self):
        current_cell: Cell = self.focused
        current_cell.toggle_class("painted")


if __name__ == "__main__":
    app = PycrossApp()
    app.run()