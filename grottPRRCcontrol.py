# module to control inverter export power via default PRRC inputs

import RPi.GPIO as GPIO

class grottPRRCgpio:
    currentProxy = None
    pins = [4,17,27,22]
    GPIO.setmode(GPIO.BCM)

    

    def __init__(self, proxy):
        print("initiating PRRC control throug GPIO..")
        self.currentProxy = proxy

        self.currentProxy.testPrint()

        for pin in self.pins:
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)