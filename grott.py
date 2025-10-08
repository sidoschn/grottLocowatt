#Grott Growatt monitor based on TCPIP sniffing or proxy (new 2.0) 
#             
#       Monitor needs to run on a (linux) system that is abble to see TCPIP that is sent from inverter to Growatt Server
#       
#       In the TCPIP sniffer mode this can be achieved by rerouting the growatt WIFI data via a Linux server with port forwarding
#
#       For more information how to see aditional documentation on github 
#
#       Monitor can run in forground and as a standard service!
#
#       For version history see: version_history.txt

# Updated: 2023-12-04

verrel = "2.8.6"

import sys

from grottconf import Conf
from grottproxy import Proxy
from grottsniffer import Sniff
import sensorGenerator
import os
import subprocess

#proces config file
conf = Conf(verrel)

#print configuration
if conf.verbose: conf.print()

print("Grott running auto-update")
#pullResult = os.system("git pull")
try:
    pullResult = subprocess.check_output("git pull", shell=True,text=True)
except:
    print("autoupdate failure, no internet connection?")
    pullResult = "cannot resolve git link"

if pullResult[0:7] == "Already":
    print("grottLocowatt is up to date!")
elif pullResult[0:7] == "Updatin":
    print("update recieved, restarting grott to apply changes...")
    argumentString = ""
    for argument in sys.argv:
         argumentString = argumentString + argument + " "
    os.system("python "+ argumentString)
    sys.exit()
else:
    print("autoupdate failure, no internet connection?")

#print("grott.py was updated")
#To test config only remove # below
#sys.exit(1)

#print("sensor list path:")
#print(conf.haDeviceConfigPath)
# sensorGenerator.checkSensors(conf.haDeviceConfigPath)

#existingSensorList = sensorGenerator.getSensors(conf.haDeviceConfigPath)

#print("first sensor")
#print(existingSensorList[0])

#print("list of devices in sensor list")
#print(sensorGenerator.getListOfDevicesFromSensorList(existingSensorList))


if conf.mode == 'proxy':
        proxy = Proxy(conf)
        try:
            proxy.main(conf)
        except KeyboardInterrupt:
            print("Ctrl C - Stopping server")
            try: 
                proxy.on_close(conf)
            except:     
                print("\t - no ports to close")
            sys.exit(1)

if conf.mode == 'sniff':
        sniff = Sniff(conf)
        try: 
            sniff.main(conf)
        except KeyboardInterrupt:
            print("Ctrl C - Stopping server")
            sys.exit(1)

else:
    print("- Grott undefined mode")
