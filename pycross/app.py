from typing import Dict, Final, Tuple

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
    def __init__(self, guides: Tuple[Tuple[int]], left_offset: int, height: int):
        self.guides = guides
        super().__init__()

        self.styles.grid_size_columns = len(guides)
        self.styles.margin = (0, 0, 0, left_offset)
        self.styles.height = height

    def compose(self) -> ComposeResult:
        for _ in self.guides:
            yield Label("\n".join(map(str, _)))


class LeftFrame(Container):
    def __init__(self, guides: Tuple[Tuple[int]], width: int):
        self.guides = guides
        super().__init__()

        self.styles.grid_size_rows = len(guides)
        self.styles.width = width

    def compose(self) -> ComposeResult:
        for _ in self.guides:
            yield Label(" ".join(map(str, _)))


class Board(Container):
    BASE_TOP_FRAME_OFFSET: Final[int] = 5 # LeftFrame right mirgin (1) + Grid left padding (1) + Cell/Tile half width (6/2)

    def __init__(self, top_guides: Tuple[Tuple[int]], left_guides: Tuple[Tuple[int]]):
        self.top_guides = top_guides
        self.left_guides = left_guides

        self._max_top_guides_len: int = len(max(top_guides, key=len))
        self._max_left_guides_len: int = len(max(left_guides, key=len))

        self._left_frame_width: int = (self._max_left_guides_len * 2) - 1
        self._top_frame_offset: int = self.BASE_TOP_FRAME_OFFSET + self._left_frame_width
        super().__init__()

    def compose(self) -> ComposeResult:
        yield TopFrame(self.top_guides, self._top_frame_offset, self._max_top_guides_len)
        yield HorizontalGroup(LeftFrame(self.left_guides, self._left_frame_width), Grid(5))


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
        top_guide = (
            (1,),
            (1, 1, 1),
            (2, 1),
            (1, 1, 1),
            (1,),
        )

        left_guide = (
            (3,),
            (1,),
            (1, 1),
            (1, 1, 1),
            (1, 1),
        )

        yield Board(top_guide, left_guide)

    def action_traverse_grid(self, x_direction: int, y_direction: int) -> None:
        grid: Grid = self.query_exactly_one(Grid)
        current_cell: Cell = self.focused

        next_x: int = current_cell.x + x_direction
        next_y: int = current_cell.y + y_direction

        if 0 <= next_x < grid.dimension and 0 <= next_y < grid.dimension:
            next_cell: Cell = self.query_exactly_one(f"#cell_{next_x}_{next_y}")
            self.set_focus(next_cell)
    
    def action_paint_tile(self):
        current_cell: Cell = self.focused
        current_cell.toggle_class("painted")


if __name__ == "__main__":
    app = PycrossApp()
    app.run()