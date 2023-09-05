import time

import pytest
from pynput.keyboard import Key, Controller
from main import RabbitGame


@pytest.fixture()
def rabbit_game():
    rabbit_game = RabbitGame(debug=True)
    rabbit_game.debug_init(rabbit_position=1,
                           carrot_position=6,
                           rabbit_hole_position=3)
    rabbit_game.start_game()
    return rabbit_game


def test_debug_init(rabbit_game):
    assert rabbit_game.game_map[1] == "r"
    assert rabbit_game.game_map[3] == "O"
    assert rabbit_game.game_map[6] == "c"


def test_map_item_random_creation():
    # test random creation of game items in game map
    for _ in range(1000):
        rabbit_game = RabbitGame()
        assert "c" in rabbit_game.game_map
        assert "r" in rabbit_game.game_map
        assert "O" in rabbit_game.game_map


def test_left_move_option(rabbit_game):
    keyboard = Controller()
    keyboard.type('a')
    print(rabbit_game.game_map)
    assert rabbit_game.game_map[0] == "r"
    assert rabbit_game.game_map[1] == "_"


def test_right_move_option(rabbit_game):
    keyboard = Controller()
    keyboard.type('d')
    assert rabbit_game.game_map[2] == "r"
    assert rabbit_game.game_map[1] == "_"


def test_jump_option(rabbit_game):
    keyboard = Controller()
    keyboard.type('dj')
    assert rabbit_game.game_map[4] == "r"
    assert rabbit_game.game_map[1] == "_"
    assert rabbit_game.game_map[2] == "_"


def test_pick_option(rabbit_game):
    keyboard = Controller()
    keyboard.type('djdp')
    assert rabbit_game.game_map[5] == 'R'
    assert rabbit_game.game_map[6] == '_'
    assert rabbit_game.game_state["carrot_picked"] is True


def test_drop_option(rabbit_game):
    keyboard = Controller()
    keyboard.type('djdpap')
    assert rabbit_game.game_map[4] == "r"
    assert rabbit_game.game_state["carrot_picked"] is False
    assert rabbit_game.game_state["game_complete"] is True
