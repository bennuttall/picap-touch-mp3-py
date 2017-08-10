import MPR121
from gpiozero import RGBLED
from subprocess import call
import signal
import sys
import pygame
from time import sleep

sensor = MPR121.begin()
sensor.set_touch_threshold(40)
sensor.set_release_threshold(20)

led = RGBLED(6, 5, 26)

num_electrodes = 12

# handle ctrl+c gracefully
def signal_handler(signal, frame):
  light_rgb(0, 0, 0)
  sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def light_rgb(r, g, b):
    led.value = (r, g, b)

# convert mp3s to wavs with picap-samples-to-wav
light_rgb(0, 0, 1)
call("picap-samples-to-wav tracks", shell = True)
light_rgb(0, 0, 0)

# initialize mixer and pygame
pygame.mixer.pre_init(frequency = 44100, channels = 64, buffer = 1024)
pygame.init()

# load paths
paths = []
for i in range(num_electrodes):
  path = "tracks/.wavs/TRACK{0:03d}.wav".format(i)
  print "loading file: " + path

  paths.append(path)

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
      light_rgb(1, 0, 0)
    else:
      light_rgb(0, 0, 0)

  # sleep a bit
  sleep(0.01)
