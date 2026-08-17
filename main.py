#load the libs
from settings import Settings

Settings= Settings()
Settings.load(
    path="settings/data.json"
)

Settings.main()
print(f"hi '{Settings.username}'")