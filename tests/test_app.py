from typing import Tuple

import pytest

from pycross import Pycross


@pytest.mark.parametrize(
    "top_guides, left_guides",
    (
        pytest.param(
            (
                (1,),
                (1, 1, 1),
                (2, 1),
                (1, 1, 1),
            ),
            (
                (3,),
                (1,),
                (1, 1),
                (1, 1, 1),
                (1, 1),
            ),
            id = "Incorrect Top Guide"
        ),
        pytest.param(
            (
                (1,),
                (1, 1, 1),
                (2, 1),
                (1, 1, 1),
                (1,),
            ),
            (
                (3,),
                (1,),
                (1, 1, 1),
                (1, 1),
            ),
            id = "Incorrect Left Guide"
        ),
    )
)
def test_init_incorrect_guides(top_guides: Tuple[Tuple[int]], left_guides: Tuple[Tuple[int]]):
    solution: Tuple[Tuple[int]] = (
        (0, 1, 1, 1, 0),
        (0, 0, 1, 0, 0),
        (0, 1, 0, 1, 0),
        (1, 0, 1, 0, 1),
        (0, 1, 0, 1, 0),
    )

    with pytest.raises(ValueError):
        Pycross(top_guides, left_guides, solution)
