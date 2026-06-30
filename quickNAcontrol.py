# for now this is a testing round for the direct USB-Modbus-RTU communication with the Growatt inverter

import minimalmodbus
import time
import logging

class modbusRTUnaController:
    inverter = None
    device = '/dev/ttyUSB0'
    slaveAddress = 1
    stateDictionary = {0:"Inverter Off", 1:"Inverter On", 2:"Battery On", 4:"Battery Off"}
    logger = logging.getLogger()
    logging.basicConfig(filename="naControl.log",
                    format='%(asctime)s: %(levelname)s: %(message)s',
                    level=logging.INFO)

    def __init__(self):
        self.inverter = minimalmodbus.Instrument(self.device,self.slaveAddress) # throws error here if USB device not found, if the slave is not found it throws an error on access
        self.inverter.serial.baudrate = 9600
        self.inverter.close_port_after_each_call = True
        print("RTU controller initialized for "+ self.device)
    
    def switchInverterState(self, bTurnOff): # this is called from grottNAcontrol
        if bTurnOff:
            newSystemState = 0 #this is for inverter switching
            
        else:
            newSystemState = 1 #this is for inverter switching
            

        print("connecting to Slave "+str(self.slaveAddress))
        startTime = time.time()
        
        registerToSwitch = 0 #this is the on-off register of the inverter

        # if the NA controller requests the system to shut down, we check if the system is in off-grid mode. If so, the system shutdown is denied, otherwhise it is performed
        if newSystemState == 0:
            self.logger.info("checking system grid-state")
            time.sleep(0.5) #delay here to give the system time to actually go into off-grid mode during power outage, this time is empirical and still needs testing (50ms was too short)
            backupState = self.getBackupState()
            self.logger.info("grid state is "+str(backupState))
            if backupState == 0:
                self.logger.info("system is in off-grid mode, shut down request was denied")
                print("system is in off-grid mode, shut down request was denied")
            else:
                self.logger.info("system is on-grid, shutting down now..")
                self.inverter.write_register(registerToSwitch,newSystemState,0) # takes aprox 37 ms to complete, throws error if slave id is not existing
        else:
            self.inverter.write_register(registerToSwitch,newSystemState,0) # takes aprox 37 ms to complete, throws error if slave id is not existing

        endTime = time.time()

        deltaTime = endTime-startTime

        print("switched State to "+ self.stateDictionary[newSystemState] + "(took "+str(deltaTime)+"seconds)")
        
    def getBackupState(self):
        backupState = self.inverter.read_register(3282,0,4) # 0 is off-grid, 1 is on-grid, 2 is generator mode
        return backupState
    
    def switchSystemState(self, newSystemState):
        
        print("connecting to Slave "+str(self.slaveAddress))
        self.inverter.write_register(0,newSystemState,0)
        print("switched State to "+ self.stateDictionary[newSystemState])












# startTime = time.time()
# #instrument = minimalmodbus.Instrument('/dev/ttyUSB1', 1)  # port name, slave address (in decimal)
# inverter = minimalmodbus.Instrument('/dev/ttyUSB0',1) # throws error here if USB device not found, if the slave is not found it throws an error on access
# inverter.serial.baudrate = 9600
# inverter.close_port_after_each_call = True

# systemState = inverter.read_register(0,0) # takes aprox 37 ms to complete, throws error if slave id is not existing
# #time.sleep(1)
# #activePower = inverter.read_register(3,0)

# ## Read temperature (PV = ProcessValue) ##
# #temperature = instrument.read_register(289, 1)  # Registernumber, number of decimals
# #print(temperature)

# ## Change temperature setpoint (SP) ##
# #NEW_TEMPERATURE = 95
# #instrument.write_register(24, NEW_TEMPERATURE, 1)  # Registernumber, value, number of decimals for storage

# endTime = time.time()

# deltaTime = endTime-startTime

# print(systemState)
# #print(activePower)
# print(deltaTime)