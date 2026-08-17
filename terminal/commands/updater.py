import json
import shutil
import tempfile
import urllib.request
import zipfile
from pathlib import Path

class Updater:
    def __init__(self, project_path, repository):
        self.project_path= Path(project_path)
        self.repository= repository

    def merge_settings(self, old, new):
        if not isinstance(old, dict) or not isinstance(new, dict):
            return old
        for key, value in new.items():
            if key not in old:
                old[key]= value
            elif isinstance(old[key], dict) and isinstance(value, dict):
                self.merge_settings(old[key], value)
        return old

    def update_settings(self, new_settings):
        path= self.project_path / "settings" / "data.json"
        if not path.exists():
            return
        with open(path, "r", encoding="utf-8") as file:
            current= json.load(file)
        current= self.merge_settings(current, new_settings)
        with open(path, "w", encoding="utf-8") as file:
            json.dump(current, file, indent=4, ensure_ascii=False)

    def download(self, branch="main"):
        url= f"https://github.com/{self.repository}/archive/refs/heads/{branch}.zip"
        print(url)
        temporary= tempfile.mkdtemp()
        zip_path= Path(temporary) / "update.zip"
        urllib.request.urlretrieve(url, zip_path)
        return temporary, zip_path

    def install(self, zip_path, temporary):
        extract_path= Path(temporary) / "extracted"
        with zipfile.ZipFile(zip_path, "r") as zip_file:
            zip_file.extractall(extract_path)

        folders= list(extract_path.iterdir())
        if not folders:
            raise RuntimeError("Invalid GitHub archive.")

        source= folders[0]
        settings_source= source / "settings" / "data.json"
        if settings_source.exists():
            with open(settings_source, "r", encoding="utf-8") as file:
                new_settings= json.load(file)

            settings_destination= self.project_path / "settings" / "data.json"

            if settings_destination.exists():
                self.update_settings(new_settings)
            else:
                settings_destination.parent.mkdir(
                    parents=True,
                    exist_ok=True
                )

                shutil.copy2(
                    settings_source,
                    settings_destination
                )
        protected_models= {
            Path("models") / "data.json",
            Path("models") / "models",
        }

        for relative_path in protected_models:
            source_path= source / relative_path
            destination_path= self.project_path / relative_path
            if not source_path.exists():
                continue
            if destination_path.exists():
                continue

            destination_path.parent.mkdir(
                parents=True,
                exist_ok=True
            )
            if source_path.is_dir():
                shutil.copytree(
                    source_path,
                    destination_path
                )
            else:
                shutil.copy2(
                    source_path,
                    destination_path
                )

        for item in source.iterdir():
            relative_path= item.relative_to(source)

            if relative_path== Path("settings") / "data.json":
                continue
            if relative_path== Path("models") / "data.json":
                continue
            if relative_path== Path("models") / "models":
                continue
            destination= self.project_path / relative_path

            if item.is_dir():
                if destination.exists():
                    shutil.rmtree(destination)

                destination.parent.mkdir(
                    parents=True,
                    exist_ok=True
                )

                shutil.copytree(
                    item,
                    destination
                )

            else:
                destination.parent.mkdir(
                    parents=True,
                    exist_ok=True
                )

                shutil.copy2(
                    item,
                    destination
                )

    def update(self):
        temporary= None
        try:
            temporary, zip_path= self.download()
            self.install(zip_path, temporary)
            return {
                "success": True,
                "message": "CAI upgraded successfully!",
                "result": {"updated": True}
            }
        except Exception as error:
            return {
                "success": False,
                "message": f"CAI upgrade failed: {error}",
                "result": {"updated": False}
            }
        finally:
            if temporary:
                shutil.rmtree(temporary, ignore_errors=True)