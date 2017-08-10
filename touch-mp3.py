import MPR121
from gpiozero import RGBLED
import subprocess
import pygame
from pygame.mixer import Sound
from glob import glob
from time import sleep

sensor = MPR121.begin()
sensor.set_touch_threshold(40)
sensor.set_release_threshold(20)

led = RGBLED(6, 5, 26, active_high=False)

electrodes = range(12)

# convert mp3s to wavs with picap-samples-to-wav
led.blue = 1
subprocess.call("picap-samples-to-wav tracks", shell=True)
led.off()

# initialize mixer and pygame
pygame.mixer.pre_init(frequency=44100, channels=64, buffer=1024)
pygame.init()

sounds = [Sound(path) for path in glob("tracks/.wavs/*.wav")]

def play_sounds_when_touched():
    if sensor.touch_status_changed():
        sensor.update_touch_data()
        touched = [sensor.get_touch_data(e) for e in electrodes]
        new_touched = [e for e in electrodes if sensor.is_new_touch(e)]

        for e in new_touched:
            print("playing sound: {}".format(e))
            sound = sounds[e]
            sound.play()

        if any(touched):
            led.red = 1
        else:
            led.off()

running = True
while running:
    try:
        play_sounds_when_touched()
    except KeyboardInterrupt:
        led.off()
        running = False
    sleep(0.01)
