# for now this is a testing round for the direct USB-Modbus-RTU communication with the Growatt inverter

import minimalmodbus
import time


class modbusRTUnaController:
    inverter = None
    device = '/dev/ttyUSB0'
    slaveAddress = 1
    stateDictionary = {0:"Inverter Off", 1:"Inverter On", 2:"Battery On", 4:"Battery Off"}

    def __init__(self):
        self.inverter = inverter = minimalmodbus.Instrument(self.device,self.slaveAddress) # throws error here if USB device not found, if the slave is not found it throws an error on access
        self.inverter.serial.baudrate = 9600
        self.inverter.close_port_after_each_call = True
        print("RTU controller initialized for "+ self.device)
    
    def switchInverterState(self, bTurnOff):
        if bTurnOff:
            newSystemState = 0
        else:
            newSystemState = 1

        print("connecting to Slave "+str(self.slaveAddress))
        startTime = time.time()
        self.inverter.write_register(0,newSystemState,0) # takes aprox 37 ms to complete, throws error if slave id is not existing
        endTime = time.time()

        deltaTime = endTime-startTime

        print("switched State to "+ self.stateDictionary[newSystemState] + "(took "+str(deltaTime)+"seconds)")
        
    
    
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