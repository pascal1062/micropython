def execute(actual_time, start_time, stop_time):
    lights = False

    #get actual time as integer
    hour_min = int(str(actual_time[3]) + str('{:02}'.format(actual_time[4])))

    if hour_min >= start_time and hour_min < stop_time: lights = True

    return lights

#End
