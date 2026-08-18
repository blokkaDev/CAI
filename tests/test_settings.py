import json
import pytest
from settings import Settings


def test_settings_initial_values():
    settings= Settings()

    assert settings.username== "User"
    assert settings.developer is False
    assert settings.verbose is False
    assert settings.apis is False
    assert settings.model== "intent-neuralNetwork-v0.4.2"
    assert settings.logging is False
    assert settings.theme== "light"
    assert settings.notifications is True
    assert settings.settings== {}


def test_settings_load(settings_file):
    settings= Settings()

    result= settings.load(str(settings_file))

    assert result["success"] is True
    assert settings.settings["username"]== "User"


def test_settings_main(settings_file):
    settings= Settings()
    settings.load(str(settings_file))
    result= settings.main()

    assert result["username"]== "User"
    assert result["developer"] is False
    assert result["verbose"] is False
    assert result["apis"] is False
    assert result["model"]== "intent-neuralNetwork-v0.4.2"
    assert result["theme"]== "light"
    assert result["notifications"] is False


def test_settings_main_custom_values(settings_file, settings_data):
    settings_data["username"]= "Blokka"
    settings_data["developer"]["enabled"]= True
    settings_data["developer"]["verbose"]= True
    settings_data["developer"]["apis"]["enabled"]= True
    settings_data["developer"]["logging"]["enabled"]= True
    settings_data["mainModel"]["name"]= "test-model"
    settings_data["preferences"]["theme"]= "dark"
    settings_data["preferences"]["notifications"]= True

    settings_file.write_text(
        json.dumps(settings_data),
        encoding="utf-8",
    )

    settings= Settings()
    settings.load(str(settings_file))
    result= settings.main()

    assert result["username"]== "Blokka"
    assert result["developer"] is True
    assert result["verbose"] is True
    assert result["apis"] is True
    assert result["logging"]["enabled"] is True
    assert result["model"]== "test-model"
    assert result["theme"]== "dark"
    assert result["notifications"] is True


def test_settings_save(settings_file, tmp_path):
    settings= Settings()
    settings.load(str(settings_file))

    settings.settings["username"]= "TestUser"

    output= tmp_path / "saved.json"

    result= settings.save(str(output))

    assert result["success"] is True
    assert output.exists()

    saved= json.loads(output.read_text(encoding="utf-8"))
    assert saved["username"]== "TestUser"


def test_settings_save_preserves_unicode(settings_file, tmp_path):
    settings= Settings()
    settings.load(str(settings_file))

    settings.settings["username"]= "Èlìa"
    output= tmp_path / "saved.json"
    settings.save(str(output))

    saved= json.loads(output.read_text(encoding="utf-8"))
    assert saved["username"]== "Èlìa"


def test_settings_models_loader(settings_file, models_file):
    settings= Settings()
    settings.load(str(settings_file))

    models= settings.Models()
    result= models.load(str(models_file))

    assert result["success"] is True
    assert models.list["test-model"]["version"]== "1.0.0"


def test_settings_action_username_confirmed(
    settings_file,
    monkeypatch,
):
    settings= Settings()
    settings.load(str(settings_file))

    monkeypatch.setattr(
        "builtins.input",
        lambda _: "y" if "Continue" in _ else "Alice",
    )

    monkeypatch.setattr(
        settings,
        "clearWindow",
        lambda: None,
    )

    monkeypatch.setattr(
        "settings.time.sleep",
        lambda _: None,
    )

    settings.action("username")
    assert settings.settings["username"]== "Alice"


def test_settings_action_username_cancelled(
    settings_file,
    monkeypatch,
):
    settings= Settings()
    settings.load(str(settings_file))

    monkeypatch.setattr(
        "builtins.input",
        lambda _: "n",
    )

    monkeypatch.setattr(
        settings,
        "clearWindow",
        lambda: None,
    )

    monkeypatch.setattr(
        "settings.time.sleep",
        lambda _: None,
    )

    settings.action("username")
    assert settings.settings["username"]== "User"


@pytest.mark.parametrize(
    ("action", "expected"),
    [
        ("developer_enabled", True),
        ("verbose", True),
        ("apis_enabled", True),
        ("logging_enabled", True),
        ("logging_savefile", False),
        ("preferences_notifications", True),
    ],
)
def test_settings_boolean_actions(
    settings_file,
    monkeypatch,
    action,
    expected,
):
    settings= Settings()
    settings.load(str(settings_file))

    monkeypatch.setattr(
        "builtins.input",
        lambda _: "y",
    )

    monkeypatch.setattr(
        settings,
        "clearWindow",
        lambda: None,
    )

    monkeypatch.setattr(
        "settings.time.sleep",
        lambda _: None,
    )
    settings.action(action)

    if action== "developer_enabled":
        assert settings.settings["developer"]["enabled"] is expected
    elif action== "verbose":
        assert settings.settings["developer"]["verbose"] is expected
    elif action== "apis_enabled":
        assert settings.settings["developer"]["apis"]["enabled"] is expected
    elif action== "logging_enabled":
        assert settings.settings["developer"]["logging"]["enabled"] is expected
    elif action== "logging_savefile":
        assert settings.settings["developer"]["logging"]["saveToFile"] is expected
    elif action== "preferences_notifications":
        assert settings.settings["preferences"]["notifications"] is expected


def test_settings_theme_action(settings_file, monkeypatch):
    settings= Settings()
    settings.load(str(settings_file))
    answers= iter(["1"])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(answers),
    )

    monkeypatch.setattr(
        settings,
        "clearWindow",
        lambda: None,
    )

    monkeypatch.setattr(
        "settings.time.sleep",
        lambda _: None,
    )

    settings.action("preferences_theme")
    assert settings.settings["preferences"]["theme"]== "dark"


def test_settings_reset(settings_file, monkeypatch):
    settings= Settings()
    settings.load(str(settings_file))
    settings.settings["username"]= "Changed"

    monkeypatch.setattr(
        "builtins.input",
        lambda _: "y",
    )

    monkeypatch.setattr(
        settings,
        "clearWindow",
        lambda: None,
    )

    monkeypatch.setattr(
        "settings.time.sleep",
        lambda _: None,
    )

    settings.action("reset_settings")
    assert settings.settings["username"]== "User"


def test_settings_clear_window(monkeypatch):
    settings= Settings()
    calls= []

    def fake_run(command):
        calls.append(command)

    monkeypatch.setattr(
        "settings.subprocess.run",
        fake_run,
    )

    settings.clearWindow()
    assert len(calls)== 1
