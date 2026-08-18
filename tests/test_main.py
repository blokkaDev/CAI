from pathlib import Path


def test_main_exists():
    path= Path(__file__).parents[1] / "main.py"
    assert path.exists()
    assert path.is_file()


def test_required_directories_exist():
    root= Path(__file__).parents[1]

    required= [
        "interface",
        "models",
        "settings",
        "terminal",
    ]

    for directory in required:
        path= root / directory
        assert path.exists()
        assert path.is_dir()


def test_required_files_exist():
    root= Path(__file__).parents[1]

    required= [
        "main.py",
        "interface/__init__.py",
        "interface/data.json",
        "models/__init__.py",
        "models/models.json",
        "settings/__init__.py",
        "settings/data.json",
        "terminal/__init__.py",
        "terminal/data.json",
        "terminal/commands/core.py",
        "terminal/commands/cai.py",
        "terminal/commands/updater.py",
    ]

    for file in required:
        path= root / file

        assert path.exists()
        assert path.is_file()
