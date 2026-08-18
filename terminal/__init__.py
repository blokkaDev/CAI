import time
import json

from settings import Settings
from terminal.commands.core import (
    version,
    clear,
    help,
    unknown,
    source
)

from pathlib import Path
from terminal.commands.cai import CAI

class Terminal:
    def __init__(self):
        self.project_path= Path(__file__).resolve().parent.parent
        self.Settings= Settings()
        self.data= {}
        self.cai= CAI(self)
        self._last_command= ""

        self.commands= {
            "-h": help,
            "help": help,
            "--version": version,
            "clear": clear,
            "source": source
        }

    def run(self, path="terminal/data.json", settings="settings/data.json"):
        self.terminal(
            path=path,
            settings=settings
        )

    def load(self, path="terminal/data.json"):
        with open(
            path,
            "r",
            encoding="utf-8"
        ) as file:
            self.data= json.load(file)

        return {
            "success": True,
            "message": "Data loaded successfully!"
        }

    def settings(self, path="settings/data.json"):
        self.Settings.load(path=path)

        return {
            "success": True,
            "message": "Settings loaded successfully!",
            "developer": self.Settings.developer
        }
    
    def command(self, cmd):
        self._last_command= cmd
        cmd= cmd.strip()

        if not cmd:
            return {
                "message": "Type '-h' to get the command list",
                "result": {}
            }

        parts= cmd.split(maxsplit=1)

        name= parts[0].lower()
        args= parts[1] if len(parts) > 1 else ""

        #CAI commands
        if name== "cai":
            return self.cai.execute(args)

        function= self.commands.get(name)
        if function is None:
            return unknown(cmd)

        return function(self)

    def terminal(self, path="terminal/data.json", settings="settings/data.json"):
        self.load(path)
        self.settings(settings)

        self.Settings.load(settings)

        self.Settings.clearWindow()

        while True:

            cmd= input("> ")

            #Developer mode
            if not self.Settings.settings.get("developer", False).get("enabled", False):
                print(
                    "Please enable the developer mode "
                    "to run commands"
                )

                enable= input("Enable [Y/n] ")

                if enable.lower()== "y":
                    self.Settings.settings[
                        "developer"
                    ]["enabled"]= True

                    self.Settings.save(
                        path=settings
                    )
                    self.settings(settings)

                    print(
                        "Developer Mode enabled!"
                    )

                    time.sleep(1)
                    self.Settings.clearWindow()

                else:
                    print(
                        "Closing the terminal..."
                    )

                    time.sleep(1)
                    self.Settings.clearWindow()
                    break
                continue

            #Execute command
            if cmd== "exit":
                break

            response= self.command(cmd)
            print(
                response.get(
                    "message",
                    "No message provided"
                )
            )

            #Exit
            if response.get(
                "result",
                {}
            ).get("exit"):
                self.Settings.clearWindow()
                break