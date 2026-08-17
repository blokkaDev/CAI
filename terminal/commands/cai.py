import json
from terminal.commands.updater import Updater

class CAI:
    def __init__(self, terminal):
        self.terminal= terminal
        self.data= terminal.data
        self.load()

        self.commands= {
            "--version": self.version,
            "version": self.version,
            "upgrade": self.upgrade,
            "help": self.help,
            "-h": self.help,
        }

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

    def execute(self, args):
        command= args.strip().lower()
        if not command:
            return self.help()

        function= self.commands.get(command)
        if function is None:
            return {
                "message": f"Unknown CAI command: {command}",
                "result": {"success": False}
            }

        return function()

    def version(self):
        version= self.data.get("cai-version", "[none]")

        return {
            "message": f"CAI version: {version}",
            "result": {
                "success": True,
                "version": version
            }
        }

    def upgrade(self):
        repo= self.data.get("cai-repo", "[unknown]")
        self.Updater= Updater(self.terminal.project_path, self.terminal.data.get("cai-repo", "blokkaDev/CAI"))
        mss= self.Updater.update()

        return {
            "message": mss.get("message", "CAI upgrade failed"),
            "result": {
                "success": mss.get("success", False),
                "repository": repo,
                "updated": mss.get("result", {"updated": False})
            }
        }

    def help(self):
        commands= self.data.get("cai-commands", {})
        message= "CAI Commands:\n"
        for command, description in commands.items():
            message+= f"  {command:<15} - {description}\n"

        return {
            "message": message,
            "result": {
                "commands": commands
            }
        }