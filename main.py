from ota import OTAUpdater
from WIFI_CONFIG import SSID , PASSWORD
print("hello world")
url="https://raw.githubusercontent.com/Helindu666/pico_ota/"

ota_updater = OTAUpdater(SSID,PASSWORD,url,"main.py")

ota_updater.download_and_install_update_if_available()

