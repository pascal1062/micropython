
def execute(output, msg, last_msg, actual_time):
    if msg != last_msg:
        if msg = "On-15m" and output == 0:
            trigger = True
            timeout = 15
        elif msg = "On-30m" and output == 0:
            trigger = True
            timeout = 30
        elif msg = "On-45m" and output == 0:
            trigger = True
            timeout = 45
        elif msg = "On-60m" and output == 0:
            trigger = True
            timeout = 60
        elif msg = "Off":
            trigger = False
            timeout = 0

        if trigger:
            start_time = actual_time
            stop_time = start_time + (timeout * 60)
            output = 255
        else:
            start_time = 0
            stop_time = 0
            output = 0

    last_msg = msg

    if trigger:
        countdown_time = (stop_time - actual_time) / 60
        if countdown_time <= 0:
            output = 0
            trigger = False
            msg = "Off"
    else:
        countdown_time = 0


    return output, msg, last_msg, countdown_time, trigger

#Fin
