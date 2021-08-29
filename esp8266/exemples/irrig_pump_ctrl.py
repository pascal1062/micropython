import time

def execute(output, msg, last_msg, start_time, stop_time, duration):
    if msg != last_msg:
        if msg == "On" and output == 0:
            start_time = time.time()
            stop_time = start_time + (duration * 60)
            output = 255
        if msg == "Off":
            start_time = 0
            stop_time = 0
            output = 0
    last_msg = msg

    if time.time() >= stop_time: msg = "Off"
    countdown = (stop_time - time.time())/60  if (output == 255) else 0

    return output, msg, last_msg, start_time, stop_time, round(countdown,1)

#Fin
