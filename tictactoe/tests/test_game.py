import pytest

from .. import game as g


def test_moves():
    game = g.Game(".x.o.x.o.")
    assert game.moves() == (0, 2, 4, 6, 8)


def test_move_x():
    game = g.Game(".x.o.x.o.", 'x')
    game = game.move(4)
    assert game.field == ".x.oxx.o."
    assert game.turn == 'o'


def test_move_o():
    game = g.Game(".x.o.x.o.", 'o')
    game = game.move(4)
    assert game.field == ".x.oox.o."
    assert game.turn == 'x'


def test_move_invalid_move():
    game = g.Game(".x.o.x.o.", 'x')
    with pytest.raises(g.WrongMove):
        game.move(1)
    with pytest.raises(g.WrongMove):
        game.move(3)
    with pytest.raises(g.WrongMove):
        game.move(5)
    with pytest.raises(g.WrongMove):
        game.move(7)


WINS = [
    "***......",
    "...***...",
    "......***",
    "*..*..*..",
    ".*..*..*.",
    "..*..*..*",
    "*...*...*",
    "..*.*.*..",
    "***.*..*.",
]

TIES = [
    "xoooxxxxo",
    "xxoooxxox",
    "xxoooxxxo"
]


def pytest_generate_tests(metafunc):
    if 'winner' in metafunc.fixturenames:
        xwinning = [(s.replace('*', 'x'), 'x') for s in WINS]
        owinning = [(s.replace('*', 'o'), 'o') for s in WINS]
        metafunc.parametrize(('pattern', 'winner'), xwinning+owinning)
    if 'drawn' in metafunc.fixturenames:
        metafunc.parametrize('drawn', TIES)


def test_win(pattern, winner):
    game = g.Game(pattern)
    completed, winner, _ = game.completed()
    assert completed
    assert winner == winner


def test_tie(drawn):
    game = g.Game(drawn, 'x')
    completed, winner, _ = game.completed()
    assert completed
    assert winner is None


def test_incompleted():
    game = g.Game(".x.o.x.o.", 'x')
    completed, _, _ = game.completed()
    assert not completed
