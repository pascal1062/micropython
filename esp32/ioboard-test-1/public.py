"""
    inputs and outputs creation for the ioboard
"""

from universal_input import UniversalInput
from universal_output import UniversalOutput
from thermistor10KDegC import Thermistor10KCelsius
from percent0100Rev_aic import PercentReverseAIC
from on_off_bdc import OnOffBDC

#scale ranges
aic10K = Thermistor10KCelsius()
percentRev = PercentReverseAIC()
on_off = OnOffBDC()

#inputs
temperature = UniversalInput(1, "analog", aic10K)
photocell = UniversalInput(4, "analog", percentRev)
bouton = UniversalInput(8, "binary", on_off)

#outputs
sortie_1 = UniversalOutput(1, "binary")
sortie_2 = UniversalOutput(2, "binary")
sortie_3 = UniversalOutput(3, "binary")
sortie_4 = UniversalOutput(4, "binary")
sortie_5 = UniversalOutput(5, "binary")
sortie_6 = UniversalOutput(6, "binary")
sortie_7 = UniversalOutput(7, "binary")
sortie_8 = UniversalOutput(8, "binary")

#variables

#Fin
