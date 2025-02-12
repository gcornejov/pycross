from typing import Tuple

import pytest

from pycross import Pycross

@pytest.fixture
def game_parameters() -> Tuple[Tuple[int]]:
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

    return top_guides, left_guides, solution

@pytest.fixture()
def almost_solved_state() -> Tuple[Tuple[int]]:
    return [
        [0, 1, 0, 1, 0],
        [0, 0, 1, 0, 0],
        [0, 1, 0, 1, 0],
        [1, 0, 1, 0, 1],
        [0, 1, 0, 1, 0],
    ]

@pytest.fixture()
def pycross_app(game_parameters: Tuple[Tuple[int]]) -> Pycross:
    return Pycross(*game_parameters)
