#load the libs
from settings import Settings
from terminal import Terminal
from interface import Interface

import time

settingsPath= "settings/data.json"
interfacePath= "interface/data.json"

Settings= Settings()
Terminal= Terminal()
Interface= Interface()

Settings.clearWindow()

Settings.load(
    path=settingsPath
)

#Settings.setup() #With this command you can run a fast setup

Settings.main()
print(f"Welcome '{Settings.username}'")

#time.sleep(0.35)
#print("We are loading the terminal...")

#time.sleep(1)

#Terminal.terminal(
#    settings=settingsPath
#)

Interface.load(
    path=interfacePath
)

Interface.apps["terminal"]= Terminal
Interface.apps["settings"]= Settings

Interface.show()