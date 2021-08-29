import public
import time

public.sortie_1.value = 0
public.sortie_2.value = 0
public.sortie_3.value = 0
public.sortie_4.value = 0
public.sortie_5.value = 0
public.sortie_6.value = 0
public.sortie_7.value = 0
public.sortie_8.value = 0


while True:
    public.sortie_2.value = 255
    time.sleep_ms(500)
    public.sortie_2.value = 0
    time.sleep_ms(500)
    print(public.temperature.value)
    print(public.bouton.value)
    print(public.photocell.value)
    if public.photocell.value < 30: public.sortie_8.value = 255
    if public.photocell.value > 75 : public.sortie_8.value = 0
