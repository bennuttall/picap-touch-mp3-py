import MPR121
from gpiozero import RGBLED
from subprocess import call
import signal
import sys
import pygame
from glob import glob
from time import sleep

sensor = MPR121.begin()
sensor.set_touch_threshold(40)
sensor.set_release_threshold(20)

led = RGBLED(6, 5, 26)

num_electrodes = 12

# handle ctrl+c gracefully
def signal_handler(signal, frame):
  led.off()
  sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# convert mp3s to wavs with picap-samples-to-wav
led.blue = 1
call("picap-samples-to-wav tracks", shell=True)
led.off()

# initialize mixer and pygame
pygame.mixer.pre_init(frequency=44100, channels=64, buffer=1024)
pygame.init()

paths = glob("tracks/.wavs/*.wav")

while True:
    if sensor.touch_status_changed():
        sensor.update_touch_data()
        is_any_touch_registered = False

        for i in range(num_electrodes):
            if sensor.get_touch_data(i):
                # check if touch is registred to set the led status
                is_any_touch_registered = True

            if sensor.is_new_touch(i):
                # play sound associated with that touch
                print "playing sound: " + str(i)
                path = paths[i]
                sound = pygame.mixer.Sound(path)
                sound.play()

        # light up red led if we have any touch registered currently
        if is_any_touch_registered:
            led.red = 1
        else:
            led.off()

    # sleep a bit
    sleep(0.01)
