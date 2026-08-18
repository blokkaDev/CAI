import json

import pytest

from interface import Interface


def test_interface_initial_state():
    interface= Interface()
    assert interface.interface== {}
    assert interface.apps== {}


def test_interface_load(tmp_path):
    path= tmp_path / "interface.json"
    data= {
        "selections": {
            "Settings": {
                "open": "settings",
            }
        }
    }

    path.write_text(
        json.dumps(data),
        encoding="utf-8",
    )

    interface= Interface()
    result= interface.load(str(path))
    assert result["success"] is True
    assert interface.interface== data


def test_interface_load_invalid_json(tmp_path):
    path= tmp_path / "interface.json"
    path.write_text("{invalid", encoding="utf-8")

    interface= Interface()

    with pytest.raises(json.JSONDecodeError):
        interface.load(str(path))


def test_show_menu_empty():
    interface= Interface()
    interface.show_menu({})


def test_show_empty():
    interface= Interface()
    interface.show()


def test_show_menu_enter_opens_app(monkeypatch):
    interface= Interface()

    class FakeApp:
        def __init__(self):
            self.called= False

        def run(self):
            self.called= True

    app= FakeApp()
    interface.apps["test"]= app
    menu= {
        "Test": {
            "open": "test",
        }
    }

    keys= iter([
        "\r",
        "\x1b",
    ])

    monkeypatch.setattr(
        interface,
        "get_key",
        lambda: next(keys),
    )

    interface.show_menu(menu)

    assert app.called is True


def test_show_menu_escape(monkeypatch):
    interface= Interface()
    monkeypatch.setattr(
        interface,
        "get_key",
        lambda: "\x1b",
    )

    interface.show_menu(
        {
            "Test": {
                "open": "test",
            }
        }
    )


def test_show_menu_navigation(monkeypatch):
    interface= Interface()
    keys= iter([
        "\x1b[B",
        "\x1b[A",
        "\x1b",
    ])

    monkeypatch.setattr(
        interface,
        "get_key",
        lambda: next(keys),
    )

    interface.show_menu(
        {
            "First": {},
            "Second": {},
        }
    )


def test_interface_action(monkeypatch):
    interface= Interface()

    called= []

    class FakeApp:
        def action(self, action):
            called.append(action)

    interface.apps["settings"]= FakeApp()

    monkeypatch.setattr(
        "interface.termios.tcgetattr",
        lambda _: {},
    )

    monkeypatch.setattr(
        "interface.termios.tcsetattr",
        lambda *args: None,
    )

    monkeypatch.setattr(
        "interface.tty.setcbreak",
        lambda *args: None,
    )

    interface.action("settings.username")
    assert called== ["username"]


def test_interface_open(monkeypatch):
    interface= Interface()

    called= []

    class FakeApp:
        def run(self):
            called.append(True)

    interface.apps["test"]= FakeApp()

    monkeypatch.setattr(
        "interface.termios.tcgetattr",
        lambda _: {},
    )

    monkeypatch.setattr(
        "interface.termios.tcsetattr",
        lambda *args: None,
    )

    monkeypatch.setattr(
        "interface.tty.setcbreak",
        lambda *args: None,
    )

    interface.open("test")
    assert called== [True]
