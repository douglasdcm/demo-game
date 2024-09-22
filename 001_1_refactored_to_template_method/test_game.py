from main import main, Game


def test_main():
    assert main() is None


def test_loop():
    assert Game().loop() == (60, 60)
