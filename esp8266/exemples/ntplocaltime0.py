

import ntptime
import time
from machine import RTC

rtc = RTC()

def setlocaltime(starttime, offet):
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


def setoffsettime():
    year = "{:4}".format(time.localtime()[0])
    month = "{:02}".format(time.localtime()[1])
    day = "{:02}".format(time.localtime()[2])

    date_str = "{:4}/{:02}/{:02}".format(time.localtime()[0], time.localtime()[1], time.localtime()[2])
    season = ''

    summer_dst = (
        '2020/03/08',
        '2021/03/09',
        '2022/03/10'
    )

    winter_dst = (
        '2020/11/01',
        '2021/11/07',
        '2022/11/06',
        '2023/11/05',
        '2024/11/03',
        '2025/11/02',
        '2026/11/01',
        '2027/11/07',
        '2028/11/05',
    )

    for dst in summer_dst:
        if date_str == dst:
            season = 'summer'
            setlocaltime()
        break

    for dst in winter_dst:
        if date_str == dst: setlocaltime()
        break

    if


def setUTCtime():
    _server_OK = False
    _starttime = time.ticks_ms()

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

    return _server_OK, _starttime
