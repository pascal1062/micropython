
from ubinascii import hexlify
from machine import unique_id
from umqtt.simple import MQTTClient

class UMQTTClient():

    def __init__(self, server):
        self._id = hexlify(unique_id())
        self._client = MQTTClient(self._id, server)
        self._connected = False

    def do_connect(self):
        try:
            self._client.set_callback(self.sub_cb())
            self._client.connect()
            self._connected = True
        except:
            print("unable to connect to mqtt server")
            self._connected = False
            pass

    def do_disconnect(self):
        try:
            self._client.disconnect()
            self._connected = False
        except:
            print("unable to disconnect from mqtt server")
            self._connected = False
            pass

    def is_connected(self):
        return self._connected

    def sub_cb(self, topic, msg):
        return topic, msg

    def do_subscribe(self, msg):
        if self._connected: self._client.subscribe(msg)

    def do_publish(self, msg):
        if self._connected: self._client.publish(msg)

#End