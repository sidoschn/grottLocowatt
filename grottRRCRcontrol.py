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
    

    def __init__(self, proxy, conf):
        print("initiating PRRC control through GPIO..")
        self.currentProxy = proxy
        self.currentConfig = conf
        self.currentProxy.testPrint()

        for pin in self.pins:
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        self.getGPIOstates()
        self.interpretGPIOstates()
        


    def getGPIOstates(self):
        print("getting GPIO states ...")
        
        for i in range(len(self.pins)):
            self.currentGPIOstates[i] = GPIO.input(self.pins[i])
        
        print(self.currentGPIOstates)
        

    def interpretGPIOstates(self):
        print("interpreting GPIO states ...")
        match self.currentGPIOstates:
            case [0, 1, 1, 1]:
                print("set export power to 0% (of max inverter power)")
                newExportLimit = 0
            case [1, 0, 1, 1]:
                print("set export power to 30% (of max inverter power)")
                newExportLimit = 30
            case [1, 1, 0, 1]:
                print("set export power to 60% (of max inverter power)")
                newExportLimit = 60
            case [1, 1, 1, 0]:
                print("set export power to 100% (of max inverter power)")
                newExportLimit = 100
            case [1, 1, 1, 1]:
                print("RRCR is not connected, safety power down of export (to "+str(self.safetyPowerDownPercent)+"%)")
                newExportLimit = self.safetyPowerDownPercent 
            case _:
                print("undefined RRCR state, safety power down of export (to "+str(self.safetyPowerDownPercent)+"%)")
                newExportLimit = self.safetyPowerDownPercent
        
        print(newExportLimit)
        print(self.currentExportLimit)

        if not (newExportLimit == self.currentExportLimit):
            
            if not hasattr(self.currentProxy, "loggerId"):
                print("no logger has identified yet, waiting for logger...")
            else:
                print("setting export limit to new limit...")
                self.currentExportLimit = newExportLimit
                #self.currentProxy.compileCommand(self.currentProxy,self.currentConfig ,"ExportPower", newExportLimit) #still disabled for testing
        else:
            print("no change to export limit required")
            
