from picap import PiCap
from gpiozero import LED
import pygame
from pygame.mixer import Sound
from glob import glob

cap = PiCap(touch_threshold=40, release_threshold=40)
led = LED(6)

# initialize mixer and pygame
pygame.mixer.pre_init(frequency=44100, channels=64, buffer=1024)
pygame.init()

sounds = [Sound(path) for path in glob("tracks/.wavs/*.wav")]

def play_sound_and_light_led(electrode):
    sound = sounds[electrode]
    sound.play()
    led.on()

def check_touched():
    if not cap.touch.pressed:
        led.off()

cap.touch.when_pressed = play_sound_and_light_led
cap.touch.when_released = check_touched

pause()
