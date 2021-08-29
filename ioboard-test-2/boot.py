# This file is executed on every boot (including wake-boot from deepsleep)
import wifi_connect
import network_rtc
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()

wifi_connect.do_connect()
network_rtc.set_time()

#End
