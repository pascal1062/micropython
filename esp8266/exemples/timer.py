import time

class Timer:
    def __init__(self):
        self._start_time = None
        self._running = False
        self._newvalue = None
        self._lastvalue = None

    def start(self):
        """Start a new timer"""
        if self._running == False: self._start_time = time.time(); self._running = True

    def stop(self):
        """Stop the timer"""
        if self._running: self._start_time = None; self._running = False

    def running(self):
        return self._running

    def elapsed(self):
        if self._running: elaps = round(time.time() - self._start_time)
        else: elaps = 0

        return elaps

    def changed(self, t):
        if self._running: self._newvalue = round(time.time() - self._start_time)

        if ((self._newvalue % t) == 0) and (self._newvalue != self._lastvalue):
            val = True
        else:
            val = False
        self._lastvalue = self._newvalue
        return val

#End
