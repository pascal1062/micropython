'''
    Analog Value. express a full number as integer or float
'''

class AnalogValue():

    def __init__(self, instance, name):
        self._instance = instance
        self._name = name
        self._newvalue = 0
        self._lastvalue = 0

    def get_name(self):
        return self._name

    def get_value(self):
        return self._newvalue

    def set_value(self, val):
        if isinstance(val, int) or isinstance(val, float):
            self._newvalue = val
        else:
            return

    def changed(self):
        if self._newvalue != self._lastvalue:
            val = True
        else:
            val = False
        self._lastvalue = self._newvalue
        return val

    def greater(self):
        if (self._newvalue != self._lastvalue) and (self._newvalue > self._lastvalue):
            val = True
            self._lastvalue = self._newvalue
        else:
            val = False
        return val

    def smaller(self):
        if (self._newvalue != self._lastvalue) and (self._newvalue < self._lastvalue):
            val = True
            self._lastvalue = self._newvalue
        else:
            val = False
        return val

    #Set Property
    value = property(get_value, set_value)
    name = property(get_name)

#End
