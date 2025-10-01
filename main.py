import _thread
import time
import machine
from machine import Pin
import uasyncio as asyncio
from ota import OTAUpdater
from WIFI_CONFIG import SSID, PASSWORD,url

global led
ledd=Pin(27, Pin.OUT)
ledd.value(0)
global led_r
led_r = Pin(21, Pin.OUT)
global led_g
led_g = Pin(22, Pin.OUT)
global led_b
led_b = Pin(20, Pin.OUT)
global a
a=0
global b
b=0
global update_available
update_available = False


#led function
async def led():
    global b
    while not update_available:
        print(b)
        b+=1
        led_b.toggle()
        await asyncio.sleep(0.5)
        led_g.toggle()
        await asyncio.sleep(0.5)
        led_r.toggle()
        await asyncio.sleep(0.5)

# OTA update function
def ota_update(SSID, PASSWORD,url):
    while True:
        global ota_updater
        global update_available
        try:
            ledd.value(1)
            ota_updater = OTAUpdater(SSID, PASSWORD,url,"main.py")
            ota_updater.connect_wifi()
            ota_updater.check_for_updates()
            if ota_updater.update_available:
                print("Update available. Starting update...")
                update_available = True
                time.sleep(2)
                print("Update completed. Restarting...")
                break
            else:
                print("No update available.")
                del ota_updater
                update_available = False
                ledd.value(0)
        except Exception as e:
            print("Error during OTA update:", e)
            ledd.value(0)
        ledd.value(0)    
        time.sleep(8)  # Wait before retrying
        

# Main function to run tasks
async def main():
    _thread.start_new_thread(ota_update, (SSID, PASSWORD,url))
    await led()
    ota_updater.download_and_install_update_if_available()
    machine.reset()
    
    
asyncio.run(main())

