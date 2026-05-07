# for now this is a testing round for the direct USB-Modbus-RTU communication with the Growatt inverter

import minimalmodbus
import time

startTime = time.time()
#instrument = minimalmodbus.Instrument('/dev/ttyUSB1', 1)  # port name, slave address (in decimal)
inverter = minimalmodbus.Instrument('/dev/ttyUSB0',1)

inverter.serial.baudrate = 9600
inverter.close_port_after_each_call = True

systemState = inverter.read_register(0,0)
time.sleep(1)
activePower = inverter.read_register(3,0)

## Read temperature (PV = ProcessValue) ##
#temperature = instrument.read_register(289, 1)  # Registernumber, number of decimals
#print(temperature)

## Change temperature setpoint (SP) ##
#NEW_TEMPERATURE = 95
#instrument.write_register(24, NEW_TEMPERATURE, 1)  # Registernumber, value, number of decimals for storage

endTime = time.time()

deltaTime = endTime-startTime

print(systemState)
print(activePower)
print(deltaTime)