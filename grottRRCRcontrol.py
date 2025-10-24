# module to control inverter export power via default PRRC inputs

import RPi.GPIO as GPIO

class grottRRCRgpio:
    currentProxy = None
    pins = [4,17,27,22]
    GPIO.setmode(GPIO.BCM)
    currentGPIOstates = [None]*4
    safetyPowerDownPercent = 5
    currentExportLimit = None
    attachedToLogger = None
    bRRCRwasEverConnected = False
    

    def __init__(self, proxy, conf):
        print("initiating PRRC control through GPIO..")
        self.currentProxy = proxy
        self.currentConfig = conf
        #self.currentProxy.testPrint()
        self.attachedToLogger = proxy.loggerId
        for pin in self.pins:
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        self.getGPIOstates()
        self.interpretGPIOstates()
        


    def getGPIOstates(self):
       # print("getting GPIO states ...")
        
        for i in range(len(self.pins)):
            self.currentGPIOstates[i] = GPIO.input(self.pins[i])
        
        #print(self.currentGPIOstates)
        

    def interpretGPIOstates(self):
        #print("interpreting GPIO states ...")
        match self.currentGPIOstates:
            case [0, 1, 1, 1]:
                #print("set export power to 0% (of max inverter power)")
                self.bRRCRwasEverConnected = True
                newExportLimit = 0
            case [1, 0, 1, 1]:
                #print("set export power to 30% (of max inverter power)")
                self.bRRCRwasEverConnected = True
                newExportLimit = 30
            case [1, 1, 0, 1]:
                #print("set export power to 60% (of max inverter power)")
                self.bRRCRwasEverConnected = True
                newExportLimit = 60
            case [1, 1, 1, 0]:
                #print("set export power to 100% (of max inverter power)")
                self.bRRCRwasEverConnected = True
                newExportLimit = 100
            case [1, 1, 1, 1]:
                if self.bRRCRwasEverConnected:
                    print("RRCR has disconnected! Maintaining last set export limit: "+ str(self.currentExportLimit)+"% (of max inverter power)")
                    newExportLimit = self.currentExportLimit 
                else:
                    print("no RRCR is connected")
                    newExportLimit = self.currentExportLimit 
            case _:
                #print("undefined RRCR state, safety power down of export (to "+str(self.safetyPowerDownPercent)+"%)")
                newExportLimit = self.safetyPowerDownPercent
        
        #print(newExportLimit)
        #print(self.currentExportLimit)

        if not (newExportLimit == self.currentExportLimit):
            
            if not hasattr(self.currentProxy, "loggerId"):
                print("no logger has identified yet, waiting for logger...")
            else:
                print("setting export limit to "+str(newExportLimit)+"% (of max inverter power)")
                self.currentExportLimit = newExportLimit
                command = self.currentProxy.compileCommand(self.currentProxy,self.currentConfig ,"ExportPower", newExportLimit) #still disabled for testing
                print(command)
                
                #injectCommand(self,conf, command) #still disabled for testing
        else:
            print("no change to export limit required")
            
