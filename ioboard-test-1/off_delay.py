"""
    start output #1 on public.bouton pressed and stop after 5 secs delay
"""

import time
import public
from machine import UART

#global variables
last_state = False
last_time = 0

#serial port init
uart = UART(2, 9600)
uart.init(9600, bits=8, parity=None, stop=1)

def execute():
    global last_state
    global last_time

    msg = ""
    bytes = uart.readline()
    if bytes != None: msg = bytes.decode()
    reading = True if public.bouton.value == "On" else False
    reading_serial = True if msg == "Start" else False

    if reading or reading_serial != last_state:
        last_time = time.ticks_ms()
        if reading == True: public.sortie_1.value = 255
        if reading_serial == True: public.sortie_1.value = 255

    if time.ticks_diff(time.ticks_ms(), last_time) >= 5000:
        public.sortie_1.value = 0

    last_state = reading or reading_serial

# End
