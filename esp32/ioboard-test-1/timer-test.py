import machine
import time
import utime
from universal_input import UniversalInput
from universal_output import UniversalOutput
from on_off_bdc import OnOffBDC

on_off = OnOffBDC()
button = UniversalInput(8, "binary", on_off)

out_1 = UniversalOutput(1, "binary")

buttonState = False
lastButtonState = False
lastButtonTime = 0

#stop output #8 after a delay of 5 secondes

while True:
    #reading button form IO board input #8
    reading = True if button.value == "On" else False

    if reading != lastButtonState:
        lastButtonTime = time.ticks_ms()
        #if reading != buttonState: buttonState = reading
        if reading == True: out_1.set_value(255)

    if time.ticks_diff(time.ticks_ms(), lastButtonTime) >= 5000:
        out_1.set_value(0)

    lastButtonState = reading

#End
