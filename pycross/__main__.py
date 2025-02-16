from typing import Tuple

from pycross import Pycross

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

    app = Pycross(top_guides, left_guides, solution)
    app.run()
