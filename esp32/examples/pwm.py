
import machine

pwm = machine.PWM(machine.Pin(15))

#set frequency at 1 Hz
pwm.freq(1)

#set output at 100%. led full ON.
pwm.duty(1023)
#set output at 0%. led full OFF.
pwm.duty(0)
#set output at 50%. led  flashes at 500ms ON and 500ms OFF.
pwm.duty(512)
#set output at 20%. led  flashes at 200ms ON and 800ms OFF.
pwm.duty(204)

#End
