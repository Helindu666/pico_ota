import uasyncio as asyncio
import time
from machine import Pin
from ota import OTAUpdater
from WIFI_CONFIG import SSID, PASSWORD

# LED pins
led_r = Pin(20, Pin.OUT)
led_g = Pin(21, Pin.OUT)
led_b = Pin(22, Pin.OUT)

# OTA URL
url = "https://raw.githubusercontent.com/Helindu666/pico_ota/main.py"

# Counter
a = 0
b=0

async def ota_task(timeout_sec=8):
    global a
    try:
        # Run OTA in a thread with a timeout
        ota_updater = OTAUpdater(SSID,PASSWORD,url,"main.py")
        await asyncio.wait_for(asyncio.to_thread(ota_updater.download_and_install_update_if_available), timeout_sec)
        print("OTA completed successfully.")
    except asyncio.TimeoutError:
        print("OTA timed out! Continuing normal operation.")
    except Exception as e:
        print("OTA failed:", e)
    a += 1
    print("OTA attempt count:", a)

async def led_blink():
    while True:
        led_b.toggle()
        await asyncio.sleep(1)# non-blocking
        print(b)
        b+=1

async def main_loop():
    start = time.time()
    while True:
        if time.time() - start > 8:
            await ota_task(timeout_sec=8)
            start = time.time()
        await asyncio.sleep(0.1)  # give control back to asyncio

# Run asyncio event loop
async def main():
    # Run LED blinking and main loop concurrently
    await asyncio.gather(
        led_blink(),
        main_loop()
    )

asyncio.run(main())

