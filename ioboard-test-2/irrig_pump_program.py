import time

# button argument is acutal button pressed
# state argument is last button state... to compare with last button pressed
# start_time argument is the "start time" when button is pressed
# stop_time argument is the calculated stop time when button is pressed added with duration
# duration argument is desired time in *** minutes ***

def execute(button, output, state, start_time, stop_time, duration):
    if button != state:
        if output == 0:
            start_time = time.mktime(time.localtime()) #start as seconds elapsed since 2000
            stop_time = start_time + (duration * 60) #stop as seconds elapsed since 2000
        if button == "On": output = 255

    state = button

    if time.mktime(time.localtime()) >= stop_time: output = 0

    return output, state, start_time, stop_time

#End
