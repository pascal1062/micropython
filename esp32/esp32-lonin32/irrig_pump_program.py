import time

# button argument is acutal button pressed
# state argument is last button state... to compare with last button pressed
# start_time argument is the "start time" when button is pressed
# stop_time argument is the calculated stop time when button is pressed added with duration
# duration argument is desired time in *** minutes ***

def execute(output, demand, last_demand, start_time, stop_time, duration):
    if demand != last_demand:
        if output == 0 and demand == "start":
            start_time = time.mktime(time.localtime()) #start as seconds elapsed since 2000
            stop_time = start_time + (duration * 60) #stop as seconds elapsed since 2000
            output = 255

        if demand == "stop":
            stop_time = time.mktime(time.localtime()) #start as seconds elapsed since 2000
            start_time = stop_time #stop as seconds elapsed since 2000
            output = 0

    last_demand = demand

    if output == 255:
        countdown_time = (stop_time - time.mktime(time.localtime())) / 60
        if countdown_time <= 0: output = 0
    else:
        countdown_time = 0

    return output, last_demand, start_time, stop_time, countdown_time

#End
