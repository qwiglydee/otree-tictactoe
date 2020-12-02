from ..game import Game
from ..ai import GameState, DumbAgent, SmartAgent


def test_dumb_valid():
    """Test if dumb agent makes valid moves"""
    game = GameState(Game())
    agent = DumbAgent()
    completed = False
    while(not completed):
        move = agent.play(game)
        game = game.advance(move)
        completed, _, _ = game.completed()


def test_smart_valid():
    """Test if smart agent makes valid moves"""
    game = GameState(Game())
    agent = SmartAgent()
    completed = False
    while(not completed):
        move = agent.play(game)
        game = game.advance(move)
        completed, _, _ = game.completed()


SMART = [
    ("...xxX...", 'x'),
    (".x..x..X.", 'x'),
    ("x...x...X", 'x'),
    ("...xxO...", 'o'),
    (".x..x..O.", 'o'),
    ("x...x...O", 'o'),
]


def pytest_generate_tests(metafunc):
    if 'pattern' in metafunc.fixturenames:
        metafunc.parametrize(('pattern', 'player'), SMART)


def test_smart_strategy(pattern: str, player: str):
    """Test if smart agent makes smart moves"""
    initial = pattern.replace(player.upper(), '.')
    expected = pattern.index(player.upper())

    game = GameState(Game(initial, player))
    agent = SmartAgent()
    decision = agent.decide(game)
    assert decision == expected
