from network import LoRa
import socket
import time
import ubinascii

import struct

import pycom

from machine import Pin
from pysense import Pysense
from SI7006A20 import SI7006A20
py = Pysense()
si = SI7006A20(py)

# Disable Hearbeat
pycom.heartbeat(False)
pycom.rgbled(0x331000) # red


# Initialise LoRa in LORAWAN mode.
# Please pick the region that matches where you are using the device:
# Asia = LoRa.AS923
# Australia = LoRa.AU915
# Europe = LoRa.EU868
# United States = LoRa.US915

# Setup Temeprature

lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868, bandwidth=LoRa.BW_250KHZ)

# create an OTAA authentication parameters, change them to the provided credentials
app_eui = ubinascii.unhexlify('70B3D57ED003AFB6')
app_key = ubinascii.unhexlify('73802D693E0BF2E835756B7B1977F7F0')
#uncomment to use LoRaWAN application provided dev_eui
#dev_eui = ubinascii.unhexlify('70B3D549938EA1EE')

# join a network using OTAA (Over the Air Activation)
#uncomment below to use LoRaWAN application provided dev_eui
lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)
#lora.join(activation=LoRa.OTAA, auth=(dev_eui, app_eui, app_key), timeout=0)

# wait until the module has joined the network
while not lora.has_joined():
    time.sleep(2.5)
    print('Not yet joined...')

print('Joined')

pycom.rgbled(0x103300) # green

# create a LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

# set the LoRaWAN data rate
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)

# make the socket blocking
# (waits for the data to be sent and for the 2 receive windows to expire)
s.setblocking(True)

# Conf do Botao
button = Pin("P14", mode=Pin.IN, pull=Pin.PULL_UP)

#Strng de Envio
str_send = bytearray([0x03, 0x67, 0x00, 0x00, 0x04, 0x02, 0x00, 0x00])

but_ant = 1; # But anterior para debounce

# while True:
#     time.sleep(0.5)
#     if (button() == 0) & (but_ant == 1):
#         but_ant = 0
#         print("Button Pressed!!")
#         # send some data
#         temp = int(si.temperature()*10)
#
#         print("Temp: ", temp)
#
#         temp_bytes = temp.to_bytes(2,'big')
#         str_send[2] = temp_bytes[0]
#         str_send[3] = temp_bytes[1]
#         s.send(str_send)
#
#     if button() == 1:
#         but_ant = 1

while True:
    print("Time Out!!")
    # send some data
    temp = int(si.temperature()*10)
    print("Temp: ", temp, " C")
    #temp_bytes = temp.to_bytes(2,'big')
    temp_bytes = struct.pack(">H", temp)
    str_send[2] = temp_bytes[0]
    str_send[3] = temp_bytes[1]

    v_bat = int(py.read_battery_voltage() * 100)
    print("V Battery: ", v_bat, " V")
    temp_v_bat = struct.pack(">H", v_bat)
    #temp_v_bat = v_bat.to_bytes(2,'big')
    str_send[6] = temp_v_bat[0]
    str_send[7] = temp_v_bat[1]

    s.send(str_send)
    time.sleep(60)

# send some data
# s.send(bytes([0x01, 0x02, 0x03]))

# make the socket non-blocking
# (because if there's no data received it will block forever...)
# s.setblocking(False)

# get any data received (if any...)
# data = s.recv(64)
# print(data)
