import utime
from universal_input import UniversalInput
from universal_output import UniversalOutput
from thermistor10KDegC import Thermistor10KCelsius
from on_off_bdc import OnOffBDC

aic10K = Thermistor10KCelsius()
temperature = UniversalInput(1, "analog", aic10K)

on_off = OnOffBDC()
bouton = UniversalInput(8, "binary", on_off)

sortie_1 = UniversalOutput(1, "binary")
sortie_2 = UniversalOutput(2, "binary")
sortie_3 = UniversalOutput(3, "binary")
sortie_4 = UniversalOutput(4, "binary")
sortie_5 = UniversalOutput(5, "binary")
sortie_6 = UniversalOutput(6, "binary")
sortie_7 = UniversalOutput(7, "binary")
sortie_8 = UniversalOutput(8, "binary")

sleep = 200

while True:
    sortie_1.set_value(0)
    utime.sleep_ms(sleep)
    sortie_2.set_value(0)
    utime.sleep_ms(sleep)
    sortie_3.set_value(0)
    utime.sleep_ms(sleep)
    sortie_4.set_value(0)
    utime.sleep_ms(sleep)
    sortie_5.set_value(0)
    utime.sleep_ms(sleep)
    sortie_6.set_value(0)
    utime.sleep_ms(sleep)
    sortie_7.set_value(0)
    utime.sleep_ms(sleep)
    sortie_8.set_value(0)
    utime.sleep_ms(sleep)

    sortie_8.set_value(255)
    utime.sleep_ms(sleep)
    sortie_7.set_value(255)
    utime.sleep_ms(sleep)
    sortie_6.set_value(255)
    utime.sleep_ms(sleep)
    sortie_5.set_value(255)
    utime.sleep_ms(sleep)
    sortie_4.set_value(255)
    utime.sleep_ms(sleep)
    sortie_3.set_value(255)
    utime.sleep_ms(sleep)
    sortie_2.set_value(255)
    utime.sleep_ms(sleep)
    sortie_1.set_value(255)
    utime.sleep_ms(sleep)

    print(temperature.value)
    print(bouton.value)

#End
