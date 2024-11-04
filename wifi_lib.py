# Wifi_lib.py
import network
import time
from secrets import secrets

def wifi_init():
    ssid = secrets["ssid"]
    password = secrets["password"]
    
    station = network.WLAN(network.STA_IF)
    station.active(True)
    station.connect(ssid, password)
    
    while not station.isconnected():
        print("Conectando a Wi-Fi...")
        time.sleep(1)
    
    print("Conectado a Wi-Fi:", station.ifconfig())
    return station
