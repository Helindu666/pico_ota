import uasyncio as asyncio
import time
from machine import Pin
from ota import OTAUpdater
from WIFI_CONFIG import SSID, PASSWORD,url

# LED pins
global led_r
led_r = Pin(20, Pin.OUT)
global led_g
led_g = Pin(21, Pin.OUT)
global led_b
led_b = Pin(22, Pin.OUT)
global a
a=0
global b
b=0
global ota_updater
global update_available
update_available = False

# OTA update function
async def ota_update(SSID, PASSWORD,url):
    while True:
        try:
            ota_updater = OTAUpdater(SSID, PASSWORD,url,"main.py")
            if ota_updater.update_available:
                print("Update available. Starting update...")
                update_available = True
                time.sleep(2)
                print("Update completed. Restarting...")
            else:
                print("No update available.")
        except Exception as e:
            print("Error during OTA update:", e)
        await asyncio.sleep(8)  # Wait before retrying
        
#led function
async def led():
    global b
    while not update_available:
        print(b)
        b+=1
        led_b.toggle()
        await asyncio.sleep(1) 

# Main function to run tasks
async def main():
    global SSID
    global PASSWORD
    global url
    task1 = asyncio.create_task(ota_update(SSID, PASSWORD,url))
    task2 = asyncio.create_task(led())
    await asyncio.gather(task1, task2)
    if update_available:
        print("Performing OTA update and restarting...")
        ota_updater.perform_update()
        machine.reset()

asyncio.run(main())

