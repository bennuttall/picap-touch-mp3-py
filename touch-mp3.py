import MPR121
from gpiozero import RGBLED
from subprocess import call
import signal
import sys
import pygame
from pygame.mixer import Sound
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
sounds = [Sound(path) for path in paths]

while True:
    if sensor.touch_status_changed():
        sensor.update_touch_data()
        touched = [sensor.get_touch_data(n) for n in range(num_electrodes)]
        new_touched = [n for n in range(num_electrodes) if sensor.is_new_touch(n)]

        for n in new_touched:
            print("playing sound: {}".format(n))
            sound = sounds[n]
            sound.play()

        if any(touched):
            led.red = 1
        else:
            led.off()

    # sleep a bit
    sleep(0.01)
