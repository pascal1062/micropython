# This file is executed on every boot (including wake-boot from deepsleep)
import wifi_connect
import network_rtc
import gc
#import esp
#esp.osdebug(None)
#import webrepl

gc.collect()
wifi_connect.do_connect()
network_rtc.set_time()
#webrepl.start()

#End
