
def set_time():
    import network
    import urequests
    import ujson
    from machine import RTC

    url = "http://worldtimeapi.org/api/timezone/America/Toronto"
    wifi = network.WLAN(network.STA_IF)
    rtc = RTC()

    if wifi.isconnected():
        response = urequests.get(url)
        if response.status_code == 200: # query success
            print("JSON response:\n" + response.text)
            # parse JSON
            parsed = ujson.loads(response.text) # you can also use parsed = response.json()
            datetime_str = str(parsed["datetime"])
            year = int(datetime_str[0:4])
            month = int(datetime_str[5:7])
            day = int(datetime_str[8:10])
            hour = int(datetime_str[11:13])
            minute = int(datetime_str[14:16])
            second = int(datetime_str[17:19])
            subsecond = int(round(int(datetime_str[20:26]) / 10000))

            rtc.datetime((year, month, day, 0, hour, minute, second, subsecond))
            print("RTC updated\n")

#End
#time.localtime() --> (2019, 10, 6, 16, 39, 28, 6, 279)
