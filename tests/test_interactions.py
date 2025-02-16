from copy import deepcopy
from typing import List

import pytest

from pycross import Pycross
from pycross.app import GameGrid, Tile, WinnerMessage


async def test_key_paint_tile(pycross_app: Pycross):
    async with pycross_app.run_test() as pilot:
        await pilot.press("z")
        assert (
            "painted" in pycross_app.query_exactly_one("#tile_0_0").classes and
            pycross_app.game_state.state[0][0] == 1
        )


async def test_key_clear_tile(pycross_app: Pycross):
    async with pycross_app.run_test() as pilot:
        pycross_app.query_exactly_one("#tile_0_0").add_class("painted")
        pycross_app.game_state.state[0][0] = 1

        await pilot.press("z")
        assert (
            "painted" not in pycross_app.query_exactly_one("#tile_0_0").classes and
            pycross_app.game_state.state[0][0] == 0
        )


async def test_click_paint_tile(pycross_app: Pycross):
    async with pycross_app.run_test() as pilot:
        await pilot.click("#tile_0_0")
        assert (
            "painted" in pycross_app.query_exactly_one("#tile_0_0").classes and
            pycross_app.game_state.state[0][0] == 1
        )


async def test_click_clear_tile(pycross_app: Pycross):
    async with pycross_app.run_test() as pilot:
        pycross_app.query_exactly_one("#tile_0_0").add_class("painted")
        pycross_app.game_state.state[0][0] = 1

        await pilot.click("#tile_0_0")
        assert (
            "painted" not in pycross_app.query_exactly_one("#tile_0_0").classes and
            pycross_app.game_state.state[0][0] == 0
        )


@pytest.mark.parametrize(
    "start_tile_id, target_tile_id, key_press",
    (
        pytest.param("#tile_2_2", "#tile_2_1", "up", id="Move up from center"),
        pytest.param("#tile_2_2", "#tile_2_3", "down", id="Move down from center"),
        pytest.param("#tile_2_2", "#tile_1_2", "left", id="Move left from center"),
        pytest.param("#tile_2_2", "#tile_3_2", "right", id="Move right from center"),
        pytest.param("#tile_0_0", "#tile_0_0", "up", id="Keep position, can't go further up"),
        pytest.param("#tile_0_0", "#tile_0_0", "left", id="Keep position, can't go further left"),
        pytest.param("#tile_4_4", "#tile_4_4", "down", id="Keep position, can't go further down"),
        pytest.param("#tile_4_4", "#tile_4_4", "right", id="Keep position, can't go further right"),
    )
)
async def test_traverse_grid(pycross_app: Pycross, start_tile_id: str, target_tile_id: str, key_press: str):
    async with pycross_app.run_test() as pilot:
        start_tile: Tile = pycross_app.query_exactly_one(start_tile_id)
        pycross_app.set_focus(start_tile)

        await pilot.press(key_press)
        assert pycross_app.query_exactly_one(target_tile_id).has_focus


async def test_win_game(pycross_app: Pycross, almost_solved_state: List[List[int]]):
    pycross_app.game_state.state = almost_solved_state
    
    async with pycross_app.run_test() as pilot:
        await pilot.click("#tile_2_0")

        assert(
            pycross_app.game_state.solved and
            pycross_app.query_one(GameGrid).disabled and
            pycross_app.query_one(WinnerMessage).renderable and
            "visible" in pycross_app.query_one(WinnerMessage).classes
        )


async def test_replay(pycross_app: Pycross, almost_solved_state: List[List[int]]):
    initial_state: List[List[int]] = deepcopy(pycross_app.game_state.state)
    pycross_app.game_state.state = almost_solved_state

    async with pycross_app.run_test() as pilot:
        await pilot.click("#tile_2_0")
        await pilot.press("r")

        painted_tiles: List[str] = [tile.id for tile in pycross_app.query(Tile) if tile.has_class("painted")]

        assert(
            pycross_app.game_state.state == initial_state and
            not painted_tiles and
            "visible" not in pycross_app.query_one(WinnerMessage).classes and
            not pycross_app.query_one(GameGrid).disabled and
            pycross_app.query_exactly_one(f"#tile_0_0").has_focus
        )
