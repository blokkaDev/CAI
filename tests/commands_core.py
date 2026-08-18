from types import SimpleNamespace
from terminal.commands.core import (
    clear,
    help,
    source,
    unknown,
    version,
)


def test_version():
    terminal= SimpleNamespace(
        data={"version": "1.2.1"},
    )

    result= version(terminal)

    assert result["result"]["success"] is True
    assert result["result"]["version"]== "1.2.1"
    assert "1.2.1" in result["message"]


def test_version_missing():
    terminal= SimpleNamespace(
        data={},
    )

    result= version(terminal)

    assert result["result"]["success"] is True
    assert result["result"]["version"]== "[none]"


def test_help():
    terminal= SimpleNamespace(
        data={
            "commands": {
                "help": "Show help",
                "exit": "Exit",
            }
        },
    )

    result= help(terminal)

    assert result["result"]["commands"]== {
        "help": "Show help",
        "exit": "Exit",
    }

    assert "help" in result["message"]
    assert "exit" in result["message"]


def test_help_empty():
    terminal= SimpleNamespace(
        data={},
    )

    result= help(terminal)

    assert result["result"]["commands"]== {}
    assert result["message"]== "Commands:\n"


def test_unknown():
    result= unknown("foobar")

    assert result["result"]["success"] is False
    assert "foobar" in result["message"]


def test_clear(monkeypatch):
    terminal= SimpleNamespace()

    called= []

    terminal.Settings= SimpleNamespace(
        clearWindow=lambda: called.append(True),
    )

    result= clear(terminal)

    assert called== [True]
    assert result["result"]["success"] is True


def test_source_without_argument():
    terminal= SimpleNamespace(
        project_path="/project",
        _last_command="source",
    )

    result= source(terminal)

    assert result["result"]["success"] is True
    assert result["result"]["path"]== "/project"
