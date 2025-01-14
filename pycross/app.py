from itertools import cycle
from textwrap import dedent
from typing import Final, Iterator, List, Tuple

from textual.app import App, ComposeResult, RenderResult
from textual.binding import Binding
from textual.containers import Container, HorizontalGroup
from textual.events import Key
from textual.message import Message
from textual.widget import Widget
from textual.widgets import Label

DEFAULT_GRID_DIMENSION: Final[int] = 5
TILE_ID_TEMPLATE: Final[str] = "tile_%s_%s"


class WinnerMessage(Label):
    def show(self) -> None:
        self.update(
            dedent("""
                YOU WON!!!
                press "r" to replay the game.
            """)
        )
        self.add_class("visible")

    def hide(self) -> None:
        self.remove_class("visible")


class Tile(Widget, can_focus=True):
    class Painted(Message): 
        def __init__(self, x: int, y: int) -> None:
            self.x = x
            self.y = y
            super().__init__()

    def __init__(self, x: int, y: int, *args, **kwargs):
        self.x = x
        self.y = y
        super().__init__(*args, **kwargs)

        self.id = TILE_ID_TEMPLATE % (x, y)
    
    def render(self) -> RenderResult:
        return ""
    
    def on_click(self) -> None:
        self._toggle()
    
    def on_key(self, event: Key) -> None:
        if event.key == "z":
            self._toggle()

    def _toggle(self) -> None:
        self.toggle_class("painted")
        self.post_message(self.Painted(self.x, self.y))


class GameGrid(Container):
    CHECKERBOARD_PATTERN: Tuple[str] = ["checkerboard-a", "checkerboard-b"]

    def __init__(self, dimension: int = DEFAULT_GRID_DIMENSION):
        self.dimension: int = dimension
        super().__init__()

        self.styles.grid_size_rows = self.styles.grid_size_columns = dimension

    def compose(self) -> ComposeResult:
        pattern_iterator: Iterator[str] = cycle(self.CHECKERBOARD_PATTERN)

        q_tiles: int = self.dimension**2
        for i in range(q_tiles):
            x = i % self.dimension
            y = int(i / self.dimension)

            yield Tile(x, y, classes=f"{next(pattern_iterator)}")


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
    BASE_TOP_FRAME_OFFSET: Final[int] = 5 # LeftFrame right mirgin (1) + GameGrid left padding (1) + Tile half width (6/2)

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
        yield HorizontalGroup(LeftFrame(self.left_guides, self._left_frame_width), GameGrid(5))
        yield WinnerMessage()


class GameState():
    def __init__(self, solution: Tuple[Tuple[int]]):
        self.solution = solution
        self.solved: bool = False
        self.state: List[List[int]] = [
            [0] * len(self.solution) for _ in range(len(self.solution[0]))
        ]

    def update_state(self, x: int, y: int) -> bool:
        self.state[y][x] = 1 - self.state[y][x]

        return self._check_solved()

    def _check_solved(self) -> None:
        for y in range(len(self.state)):
            for x in range(len(self.state[y])):
                if self.state[y][x] != self.solution[y][x]:
                    return

        self.solved = True


class PycrossApp(App):
    TITLE = "Play Game"
    CSS_PATH = "pycross.tcss"
    BINDINGS = [
        Binding("up", "traverse_grid(0,-1)", "Move Up"),
        Binding("down", "traverse_grid(0,1)", "Move Down"),
        Binding("left", "traverse_grid(-1,0)", "Move Left"),
        Binding("right", "traverse_grid(1,0)", "Move Right"),
        Binding("r", "replay", "Replay Game")
    ]

    def __init__(self, top_guides: Tuple[Tuple[int]], left_guides: Tuple[Tuple[int]], solution: Tuple[Tuple[int]]):
        self.top_guides = top_guides
        self.left_guides = left_guides
        self.game_state = GameState(solution)

        self._check_game_parameters(solution)
        super().__init__()

    def _check_game_parameters(self, solution: Tuple[Tuple[int]]):
        if len(solution) != len(self.left_guides):
            raise ValueError("Unmatching number of rows between Solution and Left Guide")

        top_guides_len: int = len(self.top_guides)
        for row in solution:
            if len(row) != top_guides_len:
                raise ValueError("Unmatching number of columns between Solution and Top Guide")

    def compose(self) -> ComposeResult:
        yield Board(self.top_guides, self.left_guides)

    def action_traverse_grid(self, move_x: int, move_y: int) -> None:
        if isinstance(self.focused, Tile):
            next_x, next_y = self._next_position(move_x, move_y)
            self._move(next_x, next_y)

    
    def _next_position(self, move_x: int, move_y: int) -> Tuple[int]:
        current_tile: Tile = self.focused

        next_x: int = current_tile.x + move_x
        next_y: int = current_tile.y + move_y

        return next_x, next_y
    
    def _move(self, next_x: int, next_y: int) -> None:
        grid: GameGrid = self.query_exactly_one(GameGrid)

        if 0 <= next_x < grid.dimension and 0 <= next_y < grid.dimension:
            tile_id: str = TILE_ID_TEMPLATE % (next_x, next_y)
            next_tile: Tile = self.query_exactly_one(f"#{tile_id}")

            self.set_focus(next_tile)

    def action_replay(self):
        if self.query_one(GameGrid).disabled:
            self.game_state = GameState(self.game_state.solution)

            self.query(Tile).remove_class("painted")
            self.query_one(WinnerMessage).hide()
            self.query_one(GameGrid).disabled = False

            tile_id: str = TILE_ID_TEMPLATE % (0, 0)
            self.set_focus(self.query_exactly_one(f"#{tile_id}"))

    def on_tile_painted(self, message: Tile.Painted) -> None:
        self._play(message.x, message.y)

    def _play(self, x: int, y: int) -> None:
        self.game_state.update_state(x, y)

        if self.game_state.solved:
            self.query_one(GameGrid).disabled = True
            self.query_one(WinnerMessage).show()


if __name__ == "__main__":
    top_guides: Tuple[Tuple[int]] = (
        (1,),
        (1, 1, 1),
        (2, 1),
        (1, 1, 1),
        (1,),
    )

    left_guides: Tuple[Tuple[int]] = (
        (3,),
        (1,),
        (1, 1),
        (1, 1, 1),
        (1, 1),
    )

    solution: Tuple[Tuple[int]] = (
        (0, 1, 1, 1, 0),
        (0, 0, 1, 0, 0),
        (0, 1, 0, 1, 0),
        (1, 0, 1, 0, 1),
        (0, 1, 0, 1, 0),
    )

    app = PycrossApp(top_guides, left_guides, solution)
    app.run()
