# module to control inverter export power via default PRRC inputs

import RPi.GPIO as GPIO

class grottRRCRgpio:
    currentProxy = None
    pins = [4,17,27,22]
    GPIO.setmode(GPIO.BCM)
    currentGPIOstate = [None]*4
    

    def __init__(self, proxy):
        print("initiating PRRC control through GPIO..")
        self.currentProxy = proxy

        self.currentProxy.testPrint()

        for pin in self.pins:
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)


    def getGPIOstates(self):
        print("getting GPIO states ...")
        
        for i in range(len(self.pins)):
            print("")
            self.currentGPIOstate[i] = GPIO.input(self.pins[i])
        

        


    def interpretGPIOstates(self):

        pass
        