import pytest

from src.decorators import log


def test_success_console(capsys):
    @log()
    def f(x, y):
        return x + y

    f(1, 2)
    out = capsys.readouterr().out.strip()
    assert out == "f ok"


def test_error_console(capsys):
    @log()
    def g(x):
        if x < 0:
            raise ValueError("bad")
        return x

    with pytest.raises(ValueError):
        g(-5)

    out = capsys.readouterr().out.strip()
    assert out.startswith("g error: ValueError")
    assert "(-5,), {}" in out
