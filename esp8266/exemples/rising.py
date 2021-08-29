
class Trigger():

    def __init__(self, instance):
        self._name = instance
        self._newvalue = False
        self._lastvalue = False

    def rise(self, value):
        self._newvalue = value
        if (self._newvalue != self._lastvalue) and (self._newvalue == True):
            val = True
            self._lastvalue = self._newvalue
        else:
            val = False
        return val


#End
