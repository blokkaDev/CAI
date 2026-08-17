#load the libs
from settings import Settings
from terminal import Terminal

import time

settingsPath= "settings/data.json"

Settings= Settings()
Terminal= Terminal()

Settings.clearWindow()

Settings.load(
    path=settingsPath
)

#Settings.setup() #With this command you can run a fast setup

Settings.main()
print(f"hi '{Settings.username}'")

time.sleep(0.35)
print("We are loading the terminal...")

time.sleep(1)

Terminal.terminal(
    settings=settingsPath
)