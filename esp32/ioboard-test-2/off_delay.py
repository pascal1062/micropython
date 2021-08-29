
def execute(button, output, state, act_time, stamp_time):
    if button != state:
        stamp_time = act_time
        if button == "On": output = 255

    if act_time - stamp_time > 5000: output = 0

    state = button
    return output, state, stamp_time

# End
