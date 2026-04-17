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
    bRRCRisConnected = False
    bTurnOff = None
    

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
        #!! the RRCR CONTROLLER HAS BEEN REPURPOSED TO SHUT DOWN/TURN ON THE SYSTEM!!! (NA schutz kontakt)
        match self.currentGPIOstates:
            case [0, 1, 1, 1]:
                
                print("Shuting down System")
                #print("set export power to 0% (of max inverter power)")
                self.bRRCRwasEverConnected = True
                self.bRRCRisConnected = True
                newExportLimit = 0
                bTurnOff = False
            # case [1, 0, 1, 1]:
            #     #print("set export power to 30% (of max inverter power)")
            #     self.bRRCRwasEverConnected = True
            #     self.bRRCRisConnected = True
            #     newExportLimit = 30
            # case [1, 1, 0, 1]:
            #     #print("set export power to 60% (of max inverter power)")
            #     self.bRRCRwasEverConnected = True
            #     self.bRRCRisConnected = True
            #     newExportLimit = 60
            # case [1, 1, 1, 0]:
            #     #print("set export power to 100% (of max inverter power)")
            #     self.bRRCRwasEverConnected = True
            #     self.bRRCRisConnected = True
            #     newExportLimit = 100
            case [1, 1, 1, 1]:
                self.bRRCRisConnected = False
                if self.bRRCRwasEverConnected:
                    #print("RRCR has disconnected! Maintaining last set export limit: "+ str(self.currentExportLimit)+"% (of max inverter power)")
                    print("Turning on System")
                    newExportLimit = self.currentExportLimit 
                    bTurnOff = True
                else:
                    print("no NA protection connected")
                    newExportLimit = self.currentExportLimit 
            case _:
                #print("undefined RRCR state, safety power down of export (to "+str(self.safetyPowerDownPercent)+"%)")
                #newExportLimit = self.safetyPowerDownPercent
                bTurnOff = True
        
        #print(newExportLimit)
        #print(self.currentExportLimit)

        if not (bTurnOff == self.bTurnOff):
            
            if not hasattr(self.currentProxy, "loggerId"):
                print("no logger has identified yet, waiting for logger...")
            else:
                print("Setting system state to "+ str(bTurnOff))
                print("setting export limit to "+str(newExportLimit)+"% (of max inverter power)")
                self.bTurnOff = bTurnOff
                ##command = self.currentProxy.compileCommand(self.currentProxy,self.currentConfig ,"ExportPower", newExportLimit) #was disabled for testing
                command = self.currentProxy.compileCommand(self.currentConfig ,"TurnOff", bTurnOff) #still disabled for testing

                print(command)
                
                self.currentProxy.injectCommand(self.currentConfig, command) #was disabled for testing
        else:
            print("no change to export limit required, current limit is ", self.currentExportLimit ,"%")

        # if not (newExportLimit == self.currentExportLimit):
            
        #     if not hasattr(self.currentProxy, "loggerId"):
        #         print("no logger has identified yet, waiting for logger...")
        #     else:
        #         print("setting export limit to "+str(newExportLimit)+"% (of max inverter power)")
        #         self.currentExportLimit = newExportLimit
        #         ##command = self.currentProxy.compileCommand(self.currentProxy,self.currentConfig ,"ExportPower", newExportLimit) #was disabled for testing
        #         command = self.currentProxy.compileCommand(self.currentConfig ,"ExportPower", newExportLimit) #still disabled for testing
        #         print(command)
                
        #         self.currentProxy.injectCommand(self.currentConfig, command) #was disabled for testing
        # else:
        #     print("no change to export limit required, current limit is ", self.currentExportLimit ,"%")
            
