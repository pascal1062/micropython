import time
import public

scan_time = time.ticks_ms()
index = 2

def execute():
    global scan_time
    global index
    scan_rate = 200
    if time.ticks_diff(time.ticks_ms(), scan_time) >= scan_rate:
        scan_time = time.ticks_ms()

        """------- code goes here -------"""
        if index == 2: public.sortie_2.value = 255
        if index == 3: public.sortie_3.value = 255
        if index == 4: public.sortie_4.value = 255
        if index == 5: public.sortie_5.value = 255
        if index == 6: public.sortie_6.value = 255
        if index == 7: public.sortie_7.value = 255
        if index == 8: public.sortie_8.value = 255

        if index == 9:  public.sortie_8.value = 0
        if index == 10: public.sortie_7.value = 0
        if index == 11: public.sortie_6.value = 0
        if index == 12: public.sortie_5.value = 0
        if index == 13: public.sortie_4.value = 0
        if index == 14: public.sortie_3.value = 0
        if index == 15: public.sortie_2.value = 0

        index += 1
        if index > 15: index = 2

# End
