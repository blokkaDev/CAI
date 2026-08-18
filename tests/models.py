import json
import pytest
from models import Models


def test_models_initial_state():
    models= Models()

    assert models.list== {}


def test_models_load(models_file, models_data):
    models= Models()

    result= models.load(str(models_file))

    assert result["success"] is True
    assert "successfully" in result["message"]
    assert models.list== models_data


def test_models_load_empty_file(tmp_path):
    path= tmp_path / "models.json"
    path.write_text("{}", encoding="utf-8")

    models= Models()

    result= models.load(str(path))

    assert result["success"] is True
    assert models.list== {}


def test_models_load_invalid_json(tmp_path):
    path= tmp_path / "models.json"
    path.write_text("{invalid", encoding="utf-8")

    models= Models()

    with pytest.raises(json.JSONDecodeError):
        models.load(str(path))


def test_models_load_missing_file(tmp_path):
    models= Models()

    with pytest.raises(FileNotFoundError):
        models.load(str(tmp_path / "missing.json"))
