# module to control inverter on/off state through external NA protection device

import RPi.GPIO as GPIO
import threading
import time


class grottNAgpio:
    currentProxy = None
    pin = 4
    GPIO.setmode(GPIO.BCM)
    currentGPIOstate = None
    currentConfig = None
    safetyState = False
    attachedToLogger = None
    bWasEverConnected = False
    bIsConnected = False
    bTurnOn = None
    

    def __init__(self):
        print("initiating NA control through GPIO..")
        
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        naObserverThread = threading.Thread(target=self.nAobserver, daemon=True)
        naObserverThread.start()

    def nAobserver (self):
        print("NA observer is started")
        while True:
            if hasattr(self.currentProxy, "loggerId"):
                self.getGPIOstate()
                self.interpretGPIOstate()
                time.sleep(0.1)        
        
    def setProxy(self, proxy):
        self.currentProxy = proxy
        self.attachedToLogger = proxy.loggerId
        print("proxy set")

    def setConfig(self, config):
        self.currentConfig = config
        print("config set")

    def getGPIOstate(self):
        
        self.currentGPIOstate = GPIO.input(self.pin)
        
        

    def interpretGPIOstate(self):
       
        match self.currentGPIOstate:
            case 0:
                print("Turning on System")
                self.bWasEverConnected = True
                bTurnOn = False
            case 1:
                print("Shuting down System")
                bTurnOn = True
            case _:
                print("Safety shutdown, conflicting info")
                bTurnOn = True

        if not (bTurnOn == self.bTurnOn):
            print("Setting system state to "+ str(bTurnOn))
            self.bTurnOff = bTurnOn
            command = self.currentProxy.compileCommand(self.currentConfig ,"TurnOff", bTurnOn)
            print(command)
            # self.currentProxy.injectCommand(self.currentConfig, command) # command injection disabled for testing
        else:
            ...
            #print("no change to system state required system on is: " + str(bTurnOn) )