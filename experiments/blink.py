import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
LED = 21
GPIO.setup(LED, GPIO.OUT)

# function
def blink():
    ledState = False

    while True:
        ledState = not ledState
        setRedLight(ledState)
        time.sleep(0.5)

def setRedLight(ledState):
    GPIO.output(LED, ledState)
    
#blink()