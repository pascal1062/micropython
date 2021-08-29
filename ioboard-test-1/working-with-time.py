#time module
time.localtime(secs) : Convert a time expressed in seconds since the Epoch (see above) into an 8-tuple which contains
time.mktime() : This is inverse function of localtime. It’s argument is a full 8-tuple which expresses a time as per localtime. It returns an integer which is the number of seconds since Jan 1, 2000.

start = time.localtime() #stamp the start time
start_secs = time.mktime(start) #stamp the start as seconds elapsed since 2000
duration_secs = 3600 #3600 secs ... 1 hours
stop_secs = start_secs + duration_secs
stop = time.localtime(stop_secs) #return stop time as a tuple (real time)
