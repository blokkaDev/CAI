import json
import zipfile
from pathlib import Path

from terminal.commands.updater import Updater


def create_zip(tmp_path):
    zip_path= tmp_path / "update.zip"
    with zipfile.ZipFile(zip_path, "w") as archive:
        archive.writestr(
            "CAI-main/main.py",
            "print('updated')",
        )

        archive.writestr(
            "CAI-main/test.txt",
            "hello",
        )

    return zip_path


def test_updater_initialization(tmp_path):
    updater= Updater(
        tmp_path,
        "BlokkaDev/CAI",
    )
    assert updater.project_path== tmp_path
    assert updater.repository== "BlokkaDev/CAI"


def test_merge_settings():
    updater= Updater(
        Path("/tmp/project"),
        "BlokkaDev/CAI",
    )

    old= {
        "username": "Alice",
        "preferences": {
            "theme": "dark",
        },
    }

    new= {
        "username": "Default",
        "preferences": {
            "theme": "light",
            "notifications": True,
        },
        "newSetting": True,
    }

    result= updater.merge_settings(old, new)
    assert result["username"]== "Alice"
    assert result["preferences"]["theme"]== "dark"
    assert result["preferences"]["notifications"] is True
    assert result["newSetting"] is True


def test_merge_settings_invalid_old():
    updater= Updater(
        Path("/tmp/project"),
        "BlokkaDev/CAI",
    )

    result= updater.merge_settings(
        "invalid",
        {"test": True},
    )

    assert result== "invalid"


def test_merge_settings_invalid_new():
    updater= Updater(
        Path("/tmp/project"),
        "BlokkaDev/CAI",
    )

    result= updater.merge_settings(
        {"test": True},
        "invalid",
    )

    assert result== {"test": True}


def test_update_settings(tmp_path):
    project= tmp_path / "project"
    settings_dir= project / "settings"
    settings_dir.mkdir(parents=True)
    settings_path= settings_dir / "data.json"

    settings_path.write_text(
        json.dumps(
            {
                "username": "Alice",
                "preferences": {
                    "theme": "dark",
                },
            }
        ),
        encoding="utf-8",
    )

    updater= Updater(
        project,
        "BlokkaDev/CAI",
    )

    updater.update_settings(
        {
            "username": "Default",
            "preferences": {
                "theme": "light",
                "notifications": True,
            },
        }
    )

    data= json.loads(
        settings_path.read_text(encoding="utf-8")
    )

    assert data["username"]== "Alice"
    assert data["preferences"]["theme"]== "dark"
    assert data["preferences"]["notifications"] is True


def test_update_settings_missing_file(tmp_path):
    updater= Updater(
        tmp_path,
        "BlokkaDev/CAI",
    )

    updater.update_settings(
        {
            "test": True,
        }
    )


def test_download(monkeypatch, tmp_path):
    project= tmp_path / "project"
    updater= Updater(
        project,
        "BlokkaDev/CAI",
    )

    called= {}

    def fake_urlretrieve(url, destination):
        called["url"]= url
        Path(destination).write_bytes(b"test")

    monkeypatch.setattr(
        "terminal.commands.updater.urllib.request.urlretrieve",
        fake_urlretrieve,
    )

    temporary, zip_path= updater.download("main")

    try:
        assert "github.com/BlokkaDev/CAI" in called["url"]
        assert called["url"].endswith(
            "/archive/refs/heads/main.zip"
        )
        assert zip_path.exists()
    finally:
        import shutil

        shutil.rmtree(temporary, ignore_errors=True)


def test_install(tmp_path):
    project= tmp_path / "project"
    project.mkdir()
    updater= Updater(
        project,
        "BlokkaDev/CAI",
    )

    zip_path= create_zip(tmp_path)
    temporary= tmp_path / "temporary"
    temporary.mkdir()

    updater.install(
        zip_path,
        temporary,
    )

    assert (
        project / "main.py"
    ).read_text(encoding="utf-8")== "print('updated')"

    assert (
        project / "test.txt"
    ).read_text(encoding="utf-8")== "hello"


def test_update_success(monkeypatch, tmp_path):
    project= tmp_path / "project"
    project.mkdir()
    updater= Updater(
        project,
        "BlokkaDev/CAI",
    )

    def fake_download():
        zip_path= create_zip(tmp_path)

        temporary= tmp_path / "download"
        temporary.mkdir(exist_ok=True)

        return temporary, zip_path

    monkeypatch.setattr(
        updater,
        "download",
        fake_download,
    )

    result= updater.update()
    assert result["success"] is True
    assert result["result"]["updated"] is True


def test_update_failure(monkeypatch, tmp_path):
    updater= Updater(
        tmp_path,
        "BlokkaDev/CAI",
    )

    def fail():
        raise RuntimeError("network error")

    monkeypatch.setattr(
        updater,
        "download",
        fail,
    )

    result= updater.update()
    assert result["success"] is False
    assert result["result"]["updated"] is False
    assert "network error" in result["message"]
