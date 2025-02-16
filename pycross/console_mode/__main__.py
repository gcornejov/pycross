import game


if __name__ == "__main__":
    rows = [
        [3],
        [1],
        [1, 1],
        [1, 1, 1],
        [1, 1],
    ]

    columns = [
        [1],
        [1, 1, 1],
        [1, 2],
        [1, 1, 1],
        [1],
    ]

    solution = [
        [0, 1, 1, 1, 0],
        [0, 0, 1, 0, 0],
        [0, 1, 0, 1, 0],
        [1, 0, 1, 0, 1],
        [0, 1, 0, 1, 0],
    ]

    grid = game.Grid(rows, columns, solution)
    grid.start_game()
