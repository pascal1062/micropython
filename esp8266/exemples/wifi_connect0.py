
def do_connect():
    import network
    ssid = 'LandberhtNetzwerk24'
    password = 'PjCFnY+CN15vn56fp01Hu8Z@2'
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.ifconfig(('192.168.0.50','255.255.255.0','192.168.0.1','192.168.0.1'))
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.connect(ssid, password)
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())

#End
