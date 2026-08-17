def version(terminal):
    version= terminal.data.get("version", "[none]")

    return {
        "message": f"Terminal version: {version}",
        "result": {
            "success": True,
            "version": version
        }
    }

def source(terminal):
    terminal.project_path= str(terminal.project_path)
    if len(terminal._last_command.split())>1:
        terminal.project_path+= f"/{terminal._last_command.split()[1]}"

    return {
        "message": f"New path: {terminal.project_path}",
        "result": {
            "success": True,
            "path": terminal.project_path
        }
    }


def clear(terminal):
    terminal.Settings.clearWindow()

    return {
        "message": "Terminal cleared",
        "result": {
            "success": True
        }
    }


def help(terminal):
    commands= terminal.data.get("commands", {})

    message= "Commands:\n"

    for command, description in commands.items():
        message+= f"  {command:<15} - {description}\n"

    return {
        "message": message,
        "result": {
            "commands": commands
        }
    }


def unknown(command):
    return {
        "message": f"Unknown command: {command}",
        "result": {
            "success": False
        }
    }