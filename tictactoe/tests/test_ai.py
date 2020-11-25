from .. import game as g, ai


def test_dumb_valid():
    """Test if dumb agent makes valid moves"""
    game = g.Game()
    agent = ai.DumbAgent()
    completed = False
    while(not completed):
        move = agent.decide(game)
        game = game.move(move)
        completed, _, _ = game.completed()


def test_smart_valid():
    """Test if smart agent makes valid moves"""
    game = g.Game()
    agent = ai.SmartAgent()
    completed = False
    while(not completed):
        move = agent.decide(game)
        game = game.move(move)
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

    game = g.Game(initial, player)
    agent = ai.SmartAgent()
    decision = agent.decide(game)
    assert decision == expected
