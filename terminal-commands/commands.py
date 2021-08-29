//To load firmware espXXXX
esptool.py --port /dev/ttyUSB0 chip_id
esptool.py --port /dev/ttyUSB0 erase_flash
esptool.py --chip esp32 --port /dev/ttyUSB0 write_flash -z 0x1000 esp32-20180511-v1.9.4.bin
esptool.py --port /dev/ttyUSB0 --baud 460800 write_flash --flash_size=detect 0 esp8266-20200911-v1.13.bin //new...

//To load firmware pyboard ***put DFU jumper first***
sudo dfu-util --alt 0 -D pybv11-network-20191220-v1.12.dfu

//screen commands (serial repl usb only)
screen /dev/ttyUSB0 115200
screen /dev/ttyACM0 for pyboard
  to quit: crtl-a then k OR crtl-a then :quit
  crtl-d --> software reset

//ampy commands (usb only)
ampy --port /dev/ttyUSB0 ls (listing content of board)
ampy --port /dev/ttyUSB0 run test.py (runs code from host PC)
ampy --port /dev/ttyUSB0 run -n test.py (runs code from host PC no output)
ampy --port /dev/ttyUSB0 get boot.py (display file content)
ampy --port /dev/ttyUSB0 rm boot.py (remove file)
ampy --port /dev/ttyUSB0 mkdir dirname (create a folder)
ampy --port /dev/ttyUSB0 rmdir dirname (remove folder and all files)
ampy --port /dev/ttyUSB0 get boot.py boot.py (save boot.py from the board to the host PC)
ampy --port /dev/ttyUSB0 put main.py /main.py (save main.py from host PC to the board (at root))

//divers
import os, machine
os.listdir()
os.uname() #get device infomations
dir(os)
dir(machine)
dir(machine.RTC())
help(machine)

help('modules') #list all available modules
help('umqtt/simple') # list functions of that modules

//files
file = open("initialFile.txt", "r")
file.readline().rstrip("\n")
file.readline().rstrip("\n")
file = open("initialFile.txt", "a") //append to file...next line...
file.write("blablabla\n")
file.close()

//uart Serial
from machine import UART

uart = UART(2, 9600)                         # init with given baudrate *** if connected to raspberry pi 3, use /dev/ttyS0
uart.init(9600, bits=8, parity=None, stop=1) # init with given parameters
uart.init(9600, bits=8, parity=None, stop=1, tx=17, rx=16) #.....also works
  UART(2, baudrate=9600, bits=8, parity=None, stop=1, tx=17, rx=16, rts=-1, cts=-1, txbuf=256, rxbuf=256, timeout=5000, timeout_char=2)

uart.read(10)       # read 10 characters, returns a bytes object
uart.read()         # read all available characters
uart.readline()     # read a line
uart.readinto(buf)  # read and store into the given buffer
uart.write('abc')   # write the 3 characters
uart.write('abc\n')   # write the 3 characters with en of line


//install packages ****attention doit être connecté au wifi*****
import upip
upip.install("micropython-pystone_lowmem")
upip.install('micropython-mqtt')
upip.install('micropython-uasyncio') #installé sur sur esp32 2019-09-28

//compile to .mpy file (less space during import)
#from the micropython git project "micropython-git ..." go to mpy-crss folder and initiate command "make" inside this folder
#After doing this, a new folder "build" will be created and the command "mpy-cross" will be there
./mpy-cross foo.py

import machine
led = Pin(0, Pin.OUT) #Pin #0 for on board lED esp8266
led = machine.Pin(13, machine.Pin.OUT)
led.value(1)
led.value(0)

//flasher
while 1:
  led.value(not led.value())
  time.sleep(0.1)

//reseau
import network

sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect('LandberhtNetzwerk24', 'PjCFnY+CN15vn56fp01Hu8Z@2')

sta_if.isconnected() # check if connected
sta_if.ifconfig() # check IP address

//put this in boot.py
def do_connect():
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect('<essid>', '<password>')
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())

//RTC from network
import ntptime

# invoke this every hours
ntptime.NTP_DELTA = 3155691600 # means NTP_DELTA = 3155673600 + 18000 (18000 seconds from UTC, gmt-5h)
ntptime.settime()

time.localtime() # to retreive real local time (2019, 1, 20, 11, 30, 43, 6, 20)
rtc.datetime() # to retreive real local time

time.localtime()[0] # retreive year
time.localtime()[3] # retreive hour
time.localtime()[4] # retreive minutes

while True:
  m = time.localtime()[4]
  if m == 45: led.value(1)
  if m == 46:
    led.value(0)
    break
