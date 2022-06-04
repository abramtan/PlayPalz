import time
from bluetooth.ble import BeaconService
import RPi.GPIO as GPIO
import time
import datetime
import random
from PIL import Image,ImageDraw,ImageFont,ImageColor
import subprocess
import os
from pygame import mixer
import board
import neopixel
import smbus

pixels = neopixel.NeoPixel(board.D12, 16)

class Beacon:

    def __init__(self, data, address):
        self._uuid = data[0]
        self._major = data[1]
        self._minor = data[2]
        self._power = data[3]
        self._rssi = data[4]
        self._address = address

    def retValsPlease(self):
        return self._address, self._rssi
#    def __str__(self):
#        ret = "Beacon: address:{ADDR} uuid:{UUID} major:{MAJOR} " \
#              "minor:{MINOR} txpower:{POWER} rssi:{RSSI}" \
#              .format(ADDR=self._address, UUID=self._uuid, MAJOR=self._major,
#                      MINOR=self._minor, POWER=self._power, RSSI=self._rssi)
#        #return self._address, self._rssi
#        return ret

service = BeaconService()
#devices = service.scan(2)

service.start_advertising("11111111-2222-3333-4444-555555555555", 1, 1, 1, 200)

try:
    while 1:
        devices = service.scan(2)
        
        for address, data in list(devices.items()):
            b = Beacon(data, address)
            bb = b.retValsPlease()
#            print(bb[0])
#            print(bb[1])
            if bb[0]=="3C:A3:08:AC:83:A9" and int(bb[1]>-50):
                pixels.fill((1,1,1))
                print("Too close.")
                print(bb[1])
            else:
                pixels.fill((0,0,0))
                print("Good distance.")
                print(bb[1])

#3C:A3:08:AC:83:A9
#B8:27:EB:25:CB:F8

except:
    service.stop_advertising()
    pixels.fill((0,0,0))
    GPIO.cleanup()
