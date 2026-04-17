# module to control inverter on/off state through external NA protection device

import RPi.GPIO as GPIO
import threading
import time


class grottNAgpio:
    currentProxy = None
    pins = [4]
    GPIO.setmode(GPIO.BCM)
    currentGPIOstates = [None]
    currentConfig = None
    safetyState = False
    attachedToLogger = None
    bWasEverConnected = False
    bIsConnected = False
    bTurnOn = None
    

    def __init__(self):
        print("initiating NA control through GPIO..")
        
        for pin in self.pins:
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        naObserverThread = threading.Thread(target=self.nAobserver, daemon=True)
        naObserverThread.start()

    def nAobserver (self):
        print("NA observer is started")
        while True:
            if hasattr(self.currentProxy, "loggerId"):
                self.getGPIOstates()
                self.interpretGPIOstates()
                time.sleep(0.1)        
        
    def setProxy(self, proxy):
        self.currentProxy = proxy
        self.attachedToLogger = proxy.loggerId
        print("proxy set")

    def setConfig(self, config):
        self.currentConfig = config
        print("config set")

    def getGPIOstates(self):
        
        for i in range(len(self.pins)):
            self.currentGPIOstates[i] = GPIO.input(self.pins[i])
        

    def interpretGPIOstates(self):
       
        match self.currentGPIOstates[0]:
            case [0]:
                print("Turning on System")
                self.bWasEverConnected = True
                bTurnOn = False
            case [1]:
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
            self.currentProxy.injectCommand(self.currentConfig, command)
        else:
            ...
            #print("no change to system state required system on is: " + str(bTurnOn) )