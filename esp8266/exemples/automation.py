
"""
    en utilisant le @staticmethod, pas de besoin de créer une instance de Automation avant d'utiliser cette méthode.

"""

class Automation:

    def __init__(self):
        """ """

    @staticmethod
    def scale(x, x1, x2, y1, y2):
        _result = (x - x1) * (y2 - y1) / (x2 - x1) + y1

        """ limits """
        if _result >= y2: _result = y2
        if _result <= y1: _result = y1
        return _result

    @staticmethod
    def aswitch(out_val, analog_val, on_val, off_val):
        if out_val == None: out_val = False
        if on_val > off_val:
            """ cooling switch """
            if not out_val and analog_val >= on_val:
                out_val = True
            elif out_val and analog_val < off_val:
                out_val = False
        elif on_val < off_val:
            """ heating switch """
            if not out_val and analog_val <= on_val:
                out_val = True
            elif out_val and analog_val > off_val:
                out_val = False

        return out_val

# End
