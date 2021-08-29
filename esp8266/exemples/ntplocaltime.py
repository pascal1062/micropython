

import ntptime
import time
from machine import RTC

rtc = RTC()

def setlocaltime(offset):
    server_OK = False

    try:
        ntptime.host = '0.ca.pool.ntp.org'
        starttime = time.ticks_ms()
        ntptime.settime()
        server_OK = True
        print("npt server " + ntptime.host + " is OK")
    except:
        try:
            ntptime.host = '1.ca.pool.ntp.org'
            starttime = time.ticks_ms()
            ntptime.settime()
            server_OK = True
            print("npt server " + ntptime.host + " is OK")
        except:
            try:
                ntptime.host = '0.north-america.pool.ntp.org'
                starttime = time.ticks_ms()
                ntptime.settime()
                server_OK = True
                print("npt server " + ntptime.host + " is OK")
            except:
                try:
                    ntptime.host = '1.north-america.pool.ntp.org'
                    starttime = time.ticks_ms()
                    ntptime.settime()
                    server_OK = True
                    print("npt server " + ntptime.host + " is OK")
                except:
                    pass

    if server_OK:
        #eastern UTC shift time
        utc_shift = offset
        #convert actual UTC time at eastern time
        stop = time.ticks_diff(time.ticks_ms(), starttime)
        delta = round(stop/1000)
        tm = time.localtime((time.mktime(time.localtime())+delta) + utc_shift*3600)
        tm = (tm[0], tm[1], tm[2], tm[6] + 1, tm[3], tm[4], tm[5], 0)
        #Apply eastern shift and set final time
        rtc.datetime(tm)
        print("calling ntp server took "+ str(stop) + " msec")
