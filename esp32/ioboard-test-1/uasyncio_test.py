import uasyncio
from universal_input import UniversalInput
from universal_output import UniversalOutput
from on_off_bdc import OnOffBDC

on_off = OnOffBDC()

BI8 = UniversalInput(8, "binary", on_off)
BO1 = UniversalOutput(1, "binary")

async def once(bi):
    state = "Off"
    num = 0
    while True:
        if bi.value != state:
            if bi.value == "On":
                num += 1
                print(num)
                state = bi.value
                await uasyncio.sleep_ms(25)


async def flasher(output):
    while True:
        output.value = 0
        await uasyncio.sleep_ms(100)
        output.value = 255
        await uasyncio.sleep_ms(100)


loop = uasyncio.get_event_loop()
loop.create_task(once(BI8))
loop.create_task(flasher(BO1))
loop.run_forever()

#Je pourrais faire un "loop.create_task(PG1))" pour chacun des PG que je veux faire rouler.....

#Fin
