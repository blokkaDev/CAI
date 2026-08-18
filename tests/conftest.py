import json
import sys
from pathlib import Path
import pytest


@pytest.fixture
def project_root():
    return Path(__file__).resolve().parents[1]


@pytest.fixture
def settings_data():
    return {
        "username": "User",
        "developer": {
            "enabled": False,
            "verbose": False,
            "apis": {
                "enabled": False,
                "preferences": {
                    "port": "13743",
                    "host": "0.0.0.0",
                },
            },
            "logging": {
                "enabled": False,
                "level": "info",
                "saveToFile": True,
            },
        },
        "mainModel": {
            "name": "intent-neuralNetwork-v0.4.2",
            "id": "0",
        },
        "preferences": {
            "theme": "light",
            "notifications": False,
        },
        "models": {
            "intent-neuralNetwork-v0.4.2": {
                "training": {
                    "epochs": 500,
                    "batchSize": 32,
                    "learningRate": 0.01,
                },
                "temperature": 0.7,
                "embeddingSize": 768,
            },
        },
        "paths": {
            "models-list": "models/models.json",
        },
        "setupped": True,
        "configVersion": "1.1.2",
    }


@pytest.fixture
def settings_file(tmp_path, settings_data):
    path= tmp_path / "settings.json"
    path.write_text(
        json.dumps(settings_data),
        encoding="utf-8",
    )
    return path


@pytest.fixture
def models_data():
    return {
        "test-model": {
            "main": "main.py",
            "version": "1.0.0",
            "info": {
                "type": "neural-network",
                "description": "Test model",
                "author": "Test",
            },
        },
        "another-model": {
            "main": "main.py",
            "version": "2.0.0",
            "info": {
                "type": "neural-network",
                "description": "Another test model",
                "author": "Test",
            },
        },
    }


@pytest.fixture
def models_file(tmp_path, models_data):
    path= tmp_path / "models.json"
    path.write_text(
        json.dumps(models_data),
        encoding="utf-8",
    )
    return path


@pytest.fixture
def terminal_data():
    return {
        "version": "1.2.1",
        "cai-version": "2.6.8",
        "cai-repo": "BlokkaDev/CAI",
        "commands": {
            "help": "Get help",
            "exit": "Exit",
            "clear": "Clear",
            "--version": "Version",
            "cai": "CAI commands",
            "source": "Select folder",
        },
        "cai-commands": {
            "help": "CAI help",
            "--version": "CAI version",
            "upgrade": "Upgrade CAI",
        },
    }


@pytest.fixture
def terminal_file(tmp_path, terminal_data):
    path= tmp_path / "terminal.json"
    path.write_text(
        json.dumps(terminal_data),
        encoding="utf-8",
    )
    return path
