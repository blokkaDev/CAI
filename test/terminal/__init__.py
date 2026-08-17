from settings import Settings
import time

class Terminal:
    def __init__(self):
        self.Settings= Settings()
        pass

    def settings(self, path="settings/data.json"):
        #Let's load the settings from the json file path
        self.Settings.load(path=path)
        return {
            "success": True,
            "message": "Settings loaded successfully!",
            "developer": self.Settings.developer
        }

    def command():
        pass

    def terminal(self, settings="settings/data.json"):
        self.settings(settings)
        self.Settings.main()
        self.Settings.clearWindow()
        while True:
            cmd= input("> ").lower()

            #Only if the user is a developer can run the commands
            if self.Settings.developer:
                #If the user is a developer this part of the code will run every time
                if cmd== "":
                    print("Type '-h' to get the command list")
                elif cmd=="clear":
                    #With this command the developer can clear the terminal
                    self.Settings.clearWindow()
            else:
                print("Please enable the developer mode to run commands")

                dev= False

                while True:
                    enable= input("Enable [Y/n]")
                        
                    if enable.lower()== "y":
                        #Let's setup the developer mode
                        dev= True
                        print("Developer Mode enabled!")
                        self.Settings.settings["developer"]["enabled"]= dev
                        self.Settings.save(path=settings)
                        self.settings(settings)
                        self.Settings.main()
                        time.sleep(1)
                        self.Settings.clearWindow()
                        break
                    elif enable.lower()== "n":
                        print("Closing the terminal...")
                        time.sleep(1)
                        self.Settings.clearWindow()
                        break
                    else:
                        print("Please provide a valid response [Y/n]")

                if not dev:
                    break
