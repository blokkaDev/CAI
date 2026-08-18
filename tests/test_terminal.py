import json
from terminal import Terminal


def create_terminal(terminal_file):
    terminal= Terminal()
    terminal.load(str(terminal_file))
    return terminal


def test_terminal_initial_state():
    terminal= Terminal()

    assert terminal.data== {}
    assert terminal._last_command== ""
    assert terminal.commands["help"]
    assert terminal.commands["--version"]


def test_terminal_load(terminal_file, terminal_data):
    terminal= Terminal()
    result= terminal.load(str(terminal_file))

    assert result["success"] is True
    assert terminal.data== terminal_data


def test_terminal_load_invalid_json(tmp_path):
    path= tmp_path / "terminal.json"
    path.write_text("{invalid", encoding="utf-8")
    terminal= Terminal()

    import pytest

    with pytest.raises(json.JSONDecodeError):
        terminal.load(str(path))


def test_terminal_command_empty(terminal_file):
    terminal= create_terminal(terminal_file)
    result= terminal.command("")

    assert "Type '-h'" in result["message"]


def test_terminal_command_whitespace(terminal_file):
    terminal= create_terminal(terminal_file)
    result= terminal.command("   ")

    assert "Type '-h'" in result["message"]


def test_terminal_version(terminal_file):
    terminal= create_terminal(terminal_file)
    result= terminal.command("--version")

    assert result["result"]["success"] is True
    assert result["result"]["version"]== "1.2.1"


def test_terminal_help(terminal_file):
    terminal= create_terminal(terminal_file)
    result= terminal.command("help")

    assert result["result"]["commands"]== terminal.data["commands"]
    assert "help" in result["message"]


def test_terminal_unknown_command(terminal_file):
    terminal= create_terminal(terminal_file)
    result= terminal.command("does-not-exist")

    assert result["result"]["success"] is False
    assert "Unknown command" in result["message"]


def test_terminal_case_insensitive(terminal_file):
    terminal= create_terminal(terminal_file)
    result= terminal.command("HELP")

    assert result["result"]["commands"]== terminal.data["commands"]


def test_terminal_command_arguments(terminal_file):
    terminal= create_terminal(terminal_file)
    result= terminal.command("unknown argument")

    assert result["result"]["success"] is False
    assert terminal._last_command== "unknown argument"


def test_terminal_settings(
    terminal_file,
    settings_file,
):
    terminal= create_terminal(terminal_file)
    result= terminal.settings(str(settings_file))

    assert result["success"] is True
    assert result["developer"] is False


def test_terminal_clear(
    terminal_file,
    monkeypatch,
):
    terminal= create_terminal(terminal_file)

    monkeypatch.setattr(
        terminal.Settings,
        "clearWindow",
        lambda: None,
    )

    result= terminal.command("clear")
    assert result["result"]["success"] is True


def test_terminal_source(terminal_file):
    terminal= create_terminal(terminal_file)
    original= str(terminal.project_path)
    result= terminal.command("source models")

    assert result["result"]["success"] is True
    assert result["result"]["path"]== f"{original}/models"
