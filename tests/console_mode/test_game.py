import pytest

from pycross.console_mode.game import Grid


@pytest.fixture
def test_grid_data() -> tuple:
    return (
        # Rows Guides
        [[3], [1], [1, 1], [1, 1, 1], [1, 1]],
        # Columns Guides
        [[1], [1, 1, 1], [1, 2], [1, 1, 1], [1]],
        # Solution matrix
        [
            [0, 1, 1, 1, 0],
            [0, 0, 1, 0, 0],
            [0, 1, 0, 1, 0],
            [1, 0, 1, 0, 1],
            [0, 1, 0, 1, 0],
        ],
    )


@pytest.fixture
def test_grid_obj(test_grid_data: tuple) -> Grid:
    return Grid(*test_grid_data)


def test_grid(test_grid_obj: Grid):
    rows_guides: list[int] = [[3], [1], [1, 1], [1, 1, 1], [1, 1]]
    cols_guides: list[int] = [[1], [1, 1, 1], [1, 2], [1, 1, 1], [1]]
    board_matrix: list[int] = [[0] * 5 for _ in range(5)]

    assert (test_grid_obj._max_row_len == 3) and (test_grid_obj._max_col_len == 3)
    assert (test_grid_obj._rows_guides == rows_guides) and (test_grid_obj._columns_guides == cols_guides)
    assert test_grid_obj._board_matrix == board_matrix


def test_check_solution_matrix(test_grid_obj: Grid):
    solution: list[int] = [
        [0, 1, 1, 1, 0],
        [0, 0, 1, 0, 0],
        [0, 1, 0, 1, 0],
        [1, 0, 1, 0, 1],
        [0, 1, 0, 1, 0],
    ]

    checked_solution: list[int] = test_grid_obj._check_solution_matrix(solution, 5, 5)

    assert checked_solution == solution

@pytest.mark.parametrize(
    "rows",
    [
        ([0, 0, 1, 0, 0]),
        ([0, 1, 1, 1], [0, 0, 1, 0, 0])
    ]
)
def test_check_solution_matrix_exception(test_grid_obj: Grid, rows: list[int]):
    solution: list[int] = [
        *rows,
        [0, 1, 0, 1, 0],
        [1, 0, 1, 0, 1],
        [0, 1, 0, 1, 0],
    ]

    with pytest.raises(ValueError):
        test_grid_obj._check_solution_matrix(solution, 5, 5)


def test_draw_frame(test_grid_obj: Grid):
    grid_top: str = (
        "             1     1    \n"
        "             1  2  1    \n"
        "          1  1  1  1  1 "
    )
    grid_left: str = [
        "       3 ", 
        "       1 ", 
        "    1  1 ", 
        " 1  1  1 ", 
        "    1  1 "
    ]
    
    border_top, border_left = test_grid_obj._draw_frame()

    assert grid_top == border_top and grid_left == border_left

def test_draw_board(test_grid_obj: Grid):
    board_draw = (
        "             1     1    \n"
        "             1  2  1    \n"
        "          1  1  1  1  1 \n"
        "       3 [ ][ ][ ][ ][ ]\n"
        "       1 [ ][ ][ ][ ][ ]\n"
        "    1  1 [ ][ ][ ][ ][ ]\n"
        " 1  1  1 [ ][ ][ ][ ][ ]\n"
        "    1  1 [ ][ ][ ][ ][ ]\n"
    )
    
    screen_board: str = test_grid_obj._draw_board()

    assert board_draw == screen_board

@pytest.mark.parametrize(
    "p, result",
    [
        (0, True),
        (1, False),
    ]
)
def test_check_solved(test_grid_obj: Grid, p: int, result: bool):
    test_grid_obj._board_matrix = [
        [0, 1, 1, 1, 0],
        [0, 0, 1, 0, 0],
        [0, 1, p, 1, 0],
        [1, 0, 1, 0, 1],
        [0, 1, 0, 1, 0],
    ]

    solved = test_grid_obj.check_solved()

    assert solved == result

def test_draw_pixel(test_grid_obj: Grid):
    input: str = "3,3"
    board_draw: str = (
        "             1     1    \n"
        "             1  2  1    \n"
        "          1  1  1  1  1 \n"
        "       3 [ ][ ][ ][ ][ ]\n"
        "       1 [ ][ ][ ][ ][ ]\n"
        "    1  1 [ ][ ][\u25a0][ ][ ]\n"
        " 1  1  1 [ ][ ][ ][ ][ ]\n"
        "    1  1 [ ][ ][ ][ ][ ]\n"
    )

    test_grid_obj.draw_pixel(input)

    assert test_grid_obj._board_matrix[2][2] == 1
    assert board_draw == test_grid_obj._screen_board

def test_clear_pixel(test_grid_obj: Grid):
    input: str = "d/3,3"
    board_draw: str = (
        "             1     1    \n"
        "             1  2  1    \n"
        "          1  1  1  1  1 \n"
        "       3 [ ][ ][ ][ ][ ]\n"
        "       1 [ ][ ][ ][ ][ ]\n"
        "    1  1 [ ][ ][ ][ ][ ]\n"
        " 1  1  1 [ ][ ][ ][ ][ ]\n"
        "    1  1 [ ][ ][ ][ ][ ]\n"
    )
    test_grid_obj._board_matrix[2][2] = 1

    test_grid_obj.draw_pixel(input)

    assert test_grid_obj._board_matrix[2][2] == 0
    assert board_draw == test_grid_obj._screen_board

def test_draw_pixel_wrong_format(test_grid_obj: Grid):
    input: str = "3.3"
    board_draw: str = (
        "             1     1    \n"
        "             1  2  1    \n"
        "          1  1  1  1  1 \n"
        "       3 [ ][ ][ ][ ][ ]\n"
        "       1 [ ][ ][ ][ ][ ]\n"
        "    1  1 [ ][ ][ ][ ][ ]\n"
        " 1  1  1 [ ][ ][ ][ ][ ]\n"
        "    1  1 [ ][ ][ ][ ][ ]\n"
    )

    test_grid_obj.draw_pixel(input)

    assert test_grid_obj._board_matrix[2][2] == 0
    assert board_draw == test_grid_obj._screen_board

@pytest.mark.parametrize(
    "input, exception_class, out_msg",
    [
        ("x,y", ValueError, "Enter numeric (int) values for the coordinates\n"),
        ("6,2", IndexError, "Enter coordinates within the grid\n"),
    ]
)
def test_draw_pixel_exception(capfd, test_grid_obj: Grid, input: str, exception_class: Exception, out_msg: str):
    board_draw: str = (
        "             1     1    \n"
        "             1  2  1    \n"
        "          1  1  1  1  1 \n"
        "       3 [ ][ ][ ][ ][ ]\n"
        "       1 [ ][ ][ ][ ][ ]\n"
        "    1  1 [ ][ ][ ][ ][ ]\n"
        " 1  1  1 [ ][ ][ ][ ][ ]\n"
        "    1  1 [ ][ ][ ][ ][ ]\n"
    )

    test_grid_obj.draw_pixel(input)
    exc_msg: str = capfd.readouterr()[0]

    assert exc_msg == out_msg
    assert test_grid_obj._board_matrix[2][2] == 0
    assert board_draw == test_grid_obj._screen_board

def test_start_game():
    pass

def test_repr(test_grid_obj: Grid):
    board_draw: str = (
        "             1     1    \n"
        "             1  2  1    \n"
        "          1  1  1  1  1 \n"
        "       3 [ ][ ][ ][ ][ ]\n"
        "       1 [ ][ ][ ][ ][ ]\n"
        "    1  1 [ ][ ][ ][ ][ ]\n"
        " 1  1  1 [ ][ ][ ][ ][ ]\n"
        "    1  1 [ ][ ][ ][ ][ ]\n"
    )

    assert board_draw == str(test_grid_obj)
