
def do_connect():
    import network
    import time
    ssid = 'shed'
    password = 'fLpd838GsVNf8ZS'
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.ifconfig(('192.168.0.55','255.255.255.0','192.168.0.1','192.168.0.1'))
    wd = 0
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.connect(ssid, password)
        while not sta_if.isconnected():
            wd += 1
            time.sleep(1)
            if wd >= 5: break
            pass
    print('network config:', sta_if.ifconfig())

#End
