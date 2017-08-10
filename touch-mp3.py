from time import sleep
from subprocess import call
import signal, sys, pygame, MPR121
import RPi.GPIO as GPIO

try:
  sensor = MPR121.begin()
except Exception as e:
  print e
  sys.exit(1)

num_electrodes = 12

# this is the touch threshold - setting it low makes it more like a proximity trigger default value is 40 for touch
touch_threshold = 40

# this is the release threshold - must ALWAYS be smaller than the touch threshold default value is 20 for touch
release_threshold = 20

# set the thresholds
sensor.set_touch_threshold(touch_threshold)
sensor.set_release_threshold(release_threshold)

# handle ctrl+c gracefully
def signal_handler(signal, frame):
  light_rgb(0, 0, 0)
  sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# set up LED
red_led_pin = 6
green_led_pin = 5
blue_led_pin = 26

def light_rgb(r, g, b):
  # we are inverting the values, because the LED is active LOW
  # LOW - on
  # HIGH - off
  GPIO.output(red_led_pin, not r)
  GPIO.output(green_led_pin, not g)
  GPIO.output(blue_led_pin, not b)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(red_led_pin, GPIO.OUT)
GPIO.setup(green_led_pin, GPIO.OUT)
GPIO.setup(blue_led_pin, GPIO.OUT)

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
