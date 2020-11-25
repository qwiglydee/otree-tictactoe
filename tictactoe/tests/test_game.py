import pytest

from .. import game as g


def test_moves():
    game = g.Game(".x.o.x.o.")
    assert game.moves() == (0, 2, 4, 6, 8)


def test_move_x():
    game = g.Game(".x.o.x.o.", 'x')
    game = game.move(4, 'x')
    assert game.field == ".x.oxx.o."
    assert game.turn == 'o'


def test_move_o():
    game = g.Game(".x.o.x.o.", 'o')
    game = game.move(4, 'o')
    assert game.field == ".x.oox.o."
    assert game.turn == 'x'


def test_move_invalid_turn_x():
    game = g.Game(".x.o.x.o.", 'o')
    with pytest.raises(g.WrongTurn):
        game.move(4, 'x')


def test_move_invalid_turn_o():
    game = g.Game(".x.o.x.o.", 'x')
    with pytest.raises(g.WrongTurn):
        game.move(4, 'o')


def test_move_invalid_move():
    game = g.Game(".x.o.x.o.", 'x')
    with pytest.raises(g.WrongMove):
        game.move(1, 'x')
    with pytest.raises(g.WrongMove):
        game.move(3, 'x')
    with pytest.raises(g.WrongMove):
        game.move(5, 'x')
    with pytest.raises(g.WrongMove):
        game.move(7, 'x')


WINS = [
    "***......",
    "...***...",
    "......***",
    "*..*..*..",
    ".*..*..*.",
    "..*..*..*",
    "*...*...*",
    "..*.*.*.."
]


def pytest_generate_tests(metafunc):
    if 'winner' in metafunc.fixturenames:
        xwinning = [(s.replace('*', 'x'), 'x') for s in WINS]
        owinning = [(s.replace('*', 'o'), 'o') for s in WINS]
        metafunc.parametrize(('pattern', 'winner'), xwinning+owinning)


def test_completed_test(pattern, winner):
    game = g.Game(pattern)
    completed, winner, _ = game.completed()
    assert completed
    assert winner == winner
