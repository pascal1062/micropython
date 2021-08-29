'''
    Two Speed control FAN ou PUMP with internal delays between speeds. Require two binary outputs to operate.
    construct: pump = TwoSpeed(1) ... instance #1 other will be instance #2,3,4 etc...never use same instance!
    use: set to low -> pump.set_speed('Low', BO1, BO2)
         set to high -> pump.set_speed('High', BO1, BO2)
         set to off -> pump.set_speed('Off', BO1, BO2)
'''
import time

class TwoSpeed():

    def __init__(self, instance):
        self._instance = instance
        self._outhigh = False
        self._outlow = False
        self._speed = 'Off'
        self._lastspeed = self._speed
        self._interval = 0
        self._delay = 0

    def get_speed(self):
        return self._speed

    def set_speed(self, speed, outlow, outhigh):
        self._speed = speed

        if self._speed != self._lastspeed and self._speed == 'Off':
            self._outlow = False
            self._outhigh = False
            self._delay = time.ticks_ms()
            self._interval = time.ticks_ms()
            self._lastspeed = self._speed
            return

        if self._speed != self._lastspeed and time.ticks_diff(time.ticks_ms(), self._interval) <= 5000:
            return

        if self._speed != self._lastspeed:
            self._outlow = False
            self._outhigh = False
            self._delay = time.ticks_ms()
            self._interval = time.ticks_ms()
            self._lastspeed = self._speed

        if self._speed == 'Low':
            self._outhigh = False
            if time.ticks_diff(time.ticks_ms(), self._delay) > 2000 and self._outlow == False and self._outhigh == False: self._outlow = True
        elif self._speed == 'High':
            self._outlow = False
            if time.ticks_diff(time.ticks_ms(), self._delay) > 2000 and self._outhigh == False and self._outlow == False: self._outhigh = True
        else:
            self._outlow = False
            self._outhigh = False

        outlow.value = self._outlow
        outhigh.value = self._outhigh

#End
