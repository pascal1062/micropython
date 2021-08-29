import utime
from machine import RTC

rtc = RTC()
year = 2019
month = 8
day = 28
hour = 19
minute = 57
second = 0
subsecond = 0

# update internal RTC
rtc.datetime((year, month, day, 0, hour, minute, second, subsecond))

# generate formated date/time strings from internal RTC
   #date_str = "{:02}/{:02}/{:4}".format(rtc.datetime()[1], rtc.datetime()[2], rtc.datetime()[0])
   #time_str = "{:02}:{:02}:{:02}".format(rtc.datetime()[4], rtc.datetime()[5], rtc.datetime()[6])

"""
    à faire: dans le "main" : utiliser le utime.localtime() pour aller chercher la vraie heure.
    print(utime.localtime())
    date_str = "{:02}/{:02}/{:4}".format(utime.localtime()[1], utime.localtime()[2], utime.localtime()[0])
    time_str = "{:02}:{:02}:{:02}".format(utime.localtime()[3], utime.localtime()[4], utime.localtime()[5])
    faire une classe qui avec un def update() qui va updater le date_str et le time_str
    aussi:
    import time
    print(time.localtime())
"""

#End
