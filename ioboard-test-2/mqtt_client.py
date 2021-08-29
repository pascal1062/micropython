from ubinascii import hexlify
from machine import unique_id
from umqtt.robust import MQTTClient

client_id = hexlify(unique_id())
server = '192.168.0.149'
client = MQTTClient(client_id, server)

def mqtt_connect():
    import network
    wifi = network.WLAN(network.STA_IF)

    if wifi.isconnected():
        client.connect()
        return client

#End
