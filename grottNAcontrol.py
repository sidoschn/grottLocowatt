# module to control inverter on/off state through external NA protection device

import RPi.GPIO as GPIO

class grottNAgpio:
    currentProxy = None
    pins = [4]
    GPIO.setmode(GPIO.BCM)
    currentGPIOstates = [None]
    safetyState = False
    attachedToLogger = None
    bWasEverConnected = False
    bIsConnected = False
    bTurnOn = None
    

    def __init__(self, proxy, conf):
        print("initiating NA control through GPIO..")
        self.currentProxy = proxy
        self.currentConfig = conf
        self.attachedToLogger = proxy.loggerId
        for pin in self.pins:
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        self.getGPIOstates()
        self.interpretGPIOstates()
        

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
            
            if not hasattr(self.currentProxy, "loggerId"):
                print("no logger has identified yet, waiting for logger...")
            else:
                print("Setting system state to "+ str(bTurnOn))
                self.bTurnOff = bTurnOn
                command = self.currentProxy.compileCommand(self.currentConfig ,"TurnOff", bTurnOn)
                print(command)
                self.currentProxy.injectCommand(self.currentConfig, command)
        else:
            print("no change to system state required system on is: " + str(bTurnOn) )

            
