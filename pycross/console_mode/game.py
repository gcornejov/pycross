import os

class Grid:
    def __init__(
        self,
        rows_guides: list[int],
        columns_guides: list[int],
        solution_matrix: list[list[int]] = None,
    ):
        self._max_row_len: int = len(max(rows_guides, key=len))
        self._max_col_len: int = len(max(columns_guides, key=len))

        self._rows_guides: list[int] = rows_guides
        self._columns_guides: list[int] = columns_guides

        total_rows: int = len(rows_guides)
        total_cols: int = len(columns_guides)
        self._board_matrix: list[list[int]] = [
            [0] * total_cols for _ in range(total_rows)
        ]

        self._solution_matrix: list[list[int]] = self._check_solution_matrix(
            solution_matrix, total_rows, total_cols
        )

        self._top_board, self._left_board = self._draw_frame()
        self._screen_board: str = self._draw_board()

    def _check_solution_matrix(
        self, solution_matrix: list[list[int]], total_rows: int, total_columns: int
    ) -> list[list[int]]:
        if len(solution_matrix) != total_rows:
            raise ValueError("Unmatching number of rows")

        for row in solution_matrix:
            if len(row) != total_columns:
                raise ValueError("Unmatching number of columns")

        return solution_matrix

    def _draw_frame(self) -> tuple[str, list[int]]:
        top_offset: str = "   " * self._max_row_len
        top_board: str = top_offset
        for i in range(self._max_col_len - 1, -1, -1):
            for j in range(len(self._columns_guides)):
                if i < len(self._columns_guides[j]):
                    top_board += f" {str(self._columns_guides[j][i])} "
                else:
                    top_board += "   "
            if i > 0:
                top_board += f"\n{top_offset}"

        left_board: list = []
        for i in range(len(self._rows_guides)):
            guides_row: str = ""
            for j in range(self._max_row_len - 1, -1, -1):
                if j < len(self._rows_guides[i]):
                    guides_row += f" {str(self._rows_guides[i][j])} "
                else:
                    guides_row += "   "

            left_board.append(guides_row)

        return top_board, left_board

    def _draw_board(self):
        bottom_board: str = ""
        for i, guides_row in enumerate(self._left_board):
            cells = "][".join("\u25a0" if _ else " " for _ in self._board_matrix[i])
            bottom_board += f"{guides_row}[{cells}]\n"

        return f"{self._top_board}\n{bottom_board}"

    def check_solved(self) -> bool:
        for i in range(len(self._board_matrix)):
            for j in range(len(self._board_matrix[i])):
                if self._board_matrix[i][j] != self._solution_matrix[i][j]:
                    return False

        return True

    def draw_pixel(self, input: str) -> None:
        delete_pixel: bool = True if input.startswith("d/") else False
        coordinates: str = input.removeprefix("d/").split(",")

        if len(coordinates) != 2:
            print("Enter coordinates in the correct format (x,y)")
            return

        try:
            x, y = int(coordinates[0]) - 1, int(coordinates[1]) - 1
            self._board_matrix[x][y] = 0 if delete_pixel else 1
            self._screen_board = self._draw_board()
        except ValueError:
            print("Enter numeric (int) values for the coordinates")
        except IndexError:
            print("Enter coordinates within the grid")

    def start_game(self) -> None: # pragma: no cover
        win = None
        while not win:
            print(self)
            coordinates = input(
                "Enter coordinates to paint <x,y> (Prefix 'd/' to delete pixel): "
            )
            os.system("cls" if os.name == "nt" else "clear")
            self.draw_pixel(coordinates)
            win = self.check_solved()

        os.system("cls" if os.name == "nt" else "clear")
        print("You won!!!")
        print(self)

    def __repr__(self) -> str:
        return self._screen_board
