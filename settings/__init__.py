import json
from models import Models as modl
import os
import subprocess
import time

class Settings:
    def __init__(self):
        self.settings= {}
        self.username= "User"
        self.developer= False
        self.verbose= False
        self.apis= False
        self.model= "intent-neuralNetwork-v0.4.2"
        self.logging= False
        self.theme= "light"
        self.notifications= True
        self.models= {}

    def load(self, path: str="settings/data.json") -> dict:
        with open(file=path, mode="r", encoding="UTF-8") as file:
            self.settings= json.load(file)

        if not self.settings.get("setupped", False):
            self.setup(path=path)

        return {
            "success": True, 
            "message": "Settings loaded successfully!"
        }

    def main(self, values=["username", "developer", "verbose", "apis", "logging", "model", "theme", "notifications"]) -> dict:
        developer= self.settings.get("developer", False)

        #with this section of the code the settings can save parts of the settings file in vars
        if "username" in values:
            self.username= self.settings.get("username", self.username)

        if "developer" in values:
            self.developer= developer.get("enabled", self.developer)

        if "verbose" in values:
            self.verbose= developer.get("verbose", self.verbose)

        if "apis" in values:
            self.apis= developer.get("apis", self.apis).get("enabled", self.apis)

        if "logging" in values:
            self.logging= developer.get("logging", self.logging)

        if "model" in values:
            self.model= self.settings.get("mainModel", self.model).get("name", self.model)

        if "theme" in values:
            self.theme= self.settings.get("preferences", self.theme).get("theme", self.theme)

        if "notifications" in values:
            self.notifications= self.settings.get("preferences", self.notifications).get("notifications", self.notifications)

        return {
            "username": self.username,
            "developer": self.developer, 
            "verbose": self.verbose, 
            "apis": self.apis, 
            "logging": self.logging, 
            "model": self.model,
            "theme": self.theme,
            "notifications": self.notifications
        }

    class Models:
        def __init__(self):
            self.list= {}
            self.Models= modl()

        def load(self, path="models/models.json"):
            message= self.Models.load(path=path)
            self.list= self.Models.list
            return message

    def setup(self, path="settings/data.json") -> dict:
        self.clearWindow()

        print(
            f"Hey {self.settings.get('username', self.username)}, "
            "let's customize your experience:"
        )

        self.username= input("username: ")
        while len(self.username.split()) != 1 or len(self.username) > 10 or len(self.username) < 3:
            #let's verify the username
            if " " in self.username or len(self.username)>= 11:
                #it's not a bug that you can put a username directly from 'settings/data.json' bypassing these blocks

                print("Usernames must be one word and contain between 3 and 10 characters.")
                self.username= input("username: ")
            elif len(self.username)<= 2:
                print("Usernames must contain at least 3 characters")
                self.username= input("username: ")

        #Let's load all the models and print them
        models= self.Models()
        models.load(path=self.settings.get("paths", "models/models.json").get("models-list", "models/models.json"))

        print()
        print("Choose a main model:")
        ids= []
        for model in models.list:
            print(f"{model} [{len(ids)}]")
            ids.append(model)

        while True:
            try:
                modelID= int(input("Model id: "))
                try: 
                    self.model= ids[modelID]
                    break
                except IndexError:
                    print(f"Please choose a number between 0 and {len(ids) - 1}.")
            except (TypeError, ValueError):
                print("Model ID must be a number.")


        #Let the user choose the app theme
        print()
        print("Choose a theme:")

        print("Light [0]")
        print("Dark [1]")

        ids= [
            "light",
            "dark"
        ]

        while True:
            try:
                themeID= int(input("Theme id: "))
                try: 
                    self.theme= ids[themeID]
                    break
                except IndexError:
                    print(f"Please choose a number between 0 and 1.")
            except (TypeError, ValueError):
                print("Theme ID must be a number")

        #Let the user choose whether to receive notifications

        print()
        print("Do you want to receive notifications?")

        while True:
            answ= input("Notifications [Y/n]: ")
            if answ.lower()== "y":
                self.notifications= True
                break
            elif answ.lower()== "n":
                self.notifications= False
                break
            else:
                print("Please enter a valid response: [Y/n]")

        self.settings["username"]= self.username
        self.settings["mainModel"]["name"]= self.model
        self.settings["mainModel"]["id"]= modelID
        self.settings["preferences"]["theme"]= self.theme
        self.settings["preferences"]["notifications"]= self.notifications
        self.settings["setupped"]= True

        self.save(path)

        self.clearWindow()

        print("Settings saved successfully!")
        time.sleep(1)

        self.clearWindow()

    def save(self, path="settings/data.json") -> dict:
        with open(path, "w", encoding="utf-8") as file:
            json.dump(self.settings, file, indent=4)

        return {
            "success": True,
            "message": "Settings saved successfully!"
        }

    def clearWindow(self):
        if os.name== "nt":
            subprocess.run(["cmd", "/c", "cls"])
        else:
            subprocess.run(["reset"])