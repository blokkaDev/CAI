from types import SimpleNamespace
from terminal.commands.cai import CAI


def create_terminal():
    terminal= SimpleNamespace(
        data={
            "cai-version": "2.6.8",
            "cai-repo": "BlokkaDev/CAI",
            "cai-commands": {
                "help": "Get help",
                "--version": "CAI version",
                "upgrade": "Upgrade",
            },
        },
        project_path="/project",
    )

    return terminal


def test_cai_initialization(monkeypatch):
    terminal= create_terminal()
    cai= CAI(terminal)

    assert cai.terminal is terminal
    assert cai.data["cai-version"]== "2.6.8"


def test_cai_version():
    terminal= create_terminal()
    cai= CAI(terminal)
    result= cai.execute("version")

    assert result["result"]["success"] is True
    assert result["result"]["version"]== "2.6.8"


def test_cai_version_alias():
    terminal= create_terminal()
    cai= CAI(terminal)
    result= cai.execute("--version")

    assert result["result"]["success"] is True
    assert result["result"]["version"]== "2.6.8"


def test_cai_help():
    terminal= create_terminal()
    cai= CAI(terminal)
    result= cai.execute("help")

    assert result["result"]["commands"]== terminal.data["cai-commands"]


def test_cai_empty_command():
    terminal= create_terminal()
    cai= CAI(terminal)
    result= cai.execute("")

    assert result["result"]["commands"]== terminal.data["cai-commands"]


def test_cai_whitespace_command():
    terminal= create_terminal()
    cai= CAI(terminal)
    result= cai.execute("   ")

    assert result["result"]["commands"]== terminal.data["cai-commands"]


def test_cai_unknown_command():
    terminal= create_terminal()
    cai= CAI(terminal)
    result= cai.execute("unknown")

    assert result["result"]["success"] is False
    assert "Unknown CAI command" in result["message"]


def test_cai_case_insensitive():
    terminal= create_terminal()
    cai= CAI(terminal)
    result= cai.execute("VERSION")

    assert result["result"]["success"] is True
    assert result["result"]["version"]== "2.6.8"


def test_cai_upgrade(monkeypatch):
    terminal= create_terminal()
    cai= CAI(terminal)

    class FakeUpdater:
        def __init__(self, project_path, repository):
            self.project_path= project_path
            self.repository= repository

        def update(self):
            return {
                "success": True,
                "message": "Updated",
                "result": {
                    "updated": True,
                },
            }

    monkeypatch.setattr(
        "terminal.commands.cai.Updater",
        FakeUpdater,
    )

    result= cai.execute("upgrade")

    assert result["result"]["success"] is True
    assert result["result"]["updated"]["updated"] is True
    assert result["result"]["repository"]== "BlokkaDev/CAI"
