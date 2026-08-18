import json
import sys
import termios
import tty
import os
import select

class Interface:
    def __init__(self):
        self.interface= {}
        self.apps= {}

    def load(self, path="interface/data.json"):
        with open(path, "r", encoding="utf-8") as file:
            self.interface= json.load(file)
        return {
            "success": True,
            "message": "Interface Data loaded successfully!"
        }
    
    def get_key(self):
        #Get keyboard key pressed by the user
        key= os.read(sys.stdin.fileno(), 1)

        if key== b"\x1b":
            ready, _, _= select.select(
                [sys.stdin.fileno()],
                [],
                [],
                0.05
            )

            if not ready:
                return "\x1b"

            key+= os.read(sys.stdin.fileno(), 1)

            if key== b"\x1b[":
                ready, _, _= select.select(
                    [sys.stdin.fileno()],
                    [],
                    [],
                    0.05
                )

                if ready:
                    key+= os.read(sys.stdin.fileno(), 1)
            return key.decode()
        return key.decode()

    def show_menu(self, menu):
        #Show the menu elements
        elements= list(menu.keys())
        selected= 0

        if not elements:
            return
        while True:
            print("\033[2J\033[H", end="")

            for i, name in enumerate(elements):
                if i== selected:
                    print(f"> {name}")
                else:
                    print(f"  {name}")

            print("\n↑ ↓  Move")
            print("ENTER  Open")
            print("ESC    Back")

            key= self.get_key()

            if key== "\x1b[A":
                selected-= 1
                if selected < 0:
                    selected= len(elements) - 1

            elif key== "\x1b[B":
                selected+= 1
                if selected >= len(elements):
                    selected= 0

            elif key in ("\r", "\n"):
                name= elements[selected]
                element= menu[name]

                if "menu" in element:
                    self.show_menu(element["menu"])
                elif "open" in element:
                    self.open(element["open"])
                elif "action" in element:
                    self.action(element["action"])

            elif key== "\x1b":
                return

    def open(self, action):
        #Open an app
        old_settings= termios.tcgetattr(sys.stdin)

        try:
            termios.tcsetattr(
                sys.stdin,
                termios.TCSADRAIN,
                old_settings
            )
            self.apps[action].run()
        finally:
            tty.setcbreak(sys.stdin.fileno())

    def action(self, action):
        #Execute an action
        APP, ACTION= action.split(".", 1)

        old_settings= termios.tcgetattr(sys.stdin)

        try:
            termios.tcsetattr(
                sys.stdin,
                termios.TCSADRAIN,
                old_settings
            )

            self.apps[APP].action(ACTION)

        finally:
            tty.setcbreak(sys.stdin.fileno())

    def show(self):
        if not self.interface:
            return

        old_settings= termios.tcgetattr(sys.stdin)

        try:
            tty.setcbreak(sys.stdin.fileno())

            self.show_menu(
                self.interface["selections"]
            )

        finally:
            #Reset Terminal
            termios.tcsetattr(
                sys.stdin,
                termios.TCSADRAIN,
                old_settings
            )