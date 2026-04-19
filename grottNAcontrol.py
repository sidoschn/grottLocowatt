# module to control inverter on/off state through external NA protection device

import RPi.GPIO as GPIO
import threading
import time
import logging


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
    bTurnOff = None
    samplingTime = 0.05
    oversamplingTime = 0.01
    oversamplingCount = 5
    logger = logging.getLogger()
    logging.basicConfig(filename="naControl.log",
                    format='%(asctime)s: %(levelname)s: %(message)s',
                    level=logging.INFO)


    def __init__(self):
        print("initiating NA control through GPIO..")
        
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        #GPIO.add_event_detect(self.pin, GPIO.BOTH, callback=self.pinEdge,bouncetime=100)
        # GPIO.add_event_detect(self.pin, GPIO.RISING, callback=self.pinRising,bouncetime=100)
        # --switched from looped daemon thread to GPIO event handler
        naObserverThread = threading.Thread(target=self.nAobserver, daemon=True)
        naObserverThread.start()

    def nAobserver (self): #legacy
        print("NA observer is started")
        while True:
            if hasattr(self.currentProxy, "loggerId"):
                gpioState = self.getGPIOstate()
                #self.logger.info(gpioState)
                self.interpretGPIOstate(gpioState)
                
            time.sleep(self.samplingTime)        
        
    def setProxy(self, proxy):
        self.currentProxy = proxy
        self.attachedToLogger = proxy.loggerId
        print("proxy set")
        # self.getGPIOstate()
        # self.interpretGPIOstate()

    def setConfig(self, config):
        self.currentConfig = config
        print("config set")

    # def getGPIOstate(self):
    #     gpioState = GPIO.input(self.pin)
    #     self.currentGPIOstate = gpioState
    #     return gpioState
    #     #print(self.currentGPIOstate)
    
    def getGPIOstate(self):
        for i in range(self.oversamplingCount):
            partialGPIOstate =+ GPIO.input(self.pin)
            time.sleep(self.oversamplingTime)
        oversampledGPIOstate = partialGPIOstate/(self.oversamplingCount)
        self.logger.info(oversampledGPIOstate)
        gpioState = round(oversampledGPIOstate)
        self.currentGPIOstate = gpioState
        return gpioState
    # def pinFalling(self): #legacy
    #     if hasattr(self.currentProxy, "loggerId"):
    #         print("falling pin voltage")
    #         self.switchSystem(self, False)

    # def pinEdge(self): #legacy
    #     if hasattr(self.currentProxy, "loggerId"):
    #         if not (GPIO.input(self.pin)):
    #             print("falling pin voltage, switching on")
    #             self.switchSystem(self, False)
    #         else:
    #             print("rising pin voltage, shutting down")
    #             self.switchSystem(self, True)

    # def pinRising(self): #legacy
    #     if hasattr(self.currentProxy, "loggerId"):
    #         print("rising pin voltage")
            
        
    def switchSystem(self, state):
        bTurnOff = state
        print("Setting system turn off state to "+ str(bTurnOff))
        self.bTurnOff = bTurnOff
        command = self.currentProxy.compileCommand(self.currentConfig ,"TurnOff", bTurnOff)
        self.currentProxy.injectCommand(self.currentConfig, command)

    def interpretGPIOstate(self, gpioState):
        match gpioState:
        #match self.currentGPIOstate:
            case 0:
                #print("Turning on System")
                self.bWasEverConnected = True
                bTurnOff = False
            case 1:
                #print("Shuting down System")
                bTurnOff = True
            case _:
                #print("Safety shutdown, conflicting info")
                bTurnOff = True

        if not (bTurnOff == self.bTurnOff):
            self.switchSystem(bTurnOff)
        else:
            ...