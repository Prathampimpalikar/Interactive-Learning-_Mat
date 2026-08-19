import network
import time

SSID = "pratham"
PASSWORD = "pratham05"

wifi = network.WLAN(network.STA_IF)
wifi.active(True)

if not wifi.isconnected():

    print("Connecting to WiFi...")

    wifi.connect(SSID, PASSWORD)

    while not wifi.isconnected():
        time.sleep(1)

print("Connected!")
print("IP Address:", wifi.ifconfig()[0])