#Grott Growatt monitor based on TCPIP sniffing or proxy (new 2.0) 
#             
#       Monitor needs to run on a (linux) system that is able to see TCPIP that is sent from inverter to Growatt Server
#       
#       In the TCPIP sniffer mode this can be achieved by rerouting the growatt WIFI data via a Linux server with port forwarding
#
#       For more information how to see aditional documentation on github 
#
#       Monitor can run in forground and as a standard service!
#
#       For version history see: version_history.txt

# Updated: 2023-12-04



import sys
from grottconf import Conf
from grottproxy import Proxy
from grottsniffer import Sniff
import sensorGenerator
import os
import subprocess
import time
# try:
#      import psutil
#      bPsutil = True
# except:
#      print("psutil package missing")
#      bPsutil = False


verrel = "2.9.1"

#proces config file
conf = Conf(verrel)

#print configuration
if conf.verbose: conf.print()

print("Grott running auto-update ( current version is: "+verrel+" )")
#pullResult = os.system("git pull")
pullResult = "cannot resolve git link"
pullAttempt = 0
while pullResult == "cannot resolve git link":
    print("attempt "+str(pullAttempt)+" to connect to github...")
    try:
        pullResult = subprocess.check_output("git pull", shell=True,text=True)
    except:
        print("cannot resolve git link")
        pullAttempt += 1
        time.sleep(1) # this delay is added in order to give the network time to setup
        if pullAttempt > 10:
             break




if pullResult[0:7] == "Already":
    print("grottLocowatt is up to date!")
elif pullResult[0:7] == "Updatin":
    print("update recieved, closing grott to apply changes...")
    exit()
    
    # if not bPsutil:
    #      print("attempting to install missing packages")
    #      try: 
    #           installSuccess = os.system("sudo apt install python3-psutil")
    #      except:
    #           print("install failed")
        

    
    # if bPsutil:
    #      print("exiting service ...")
    #      if (psutil.Process(os.getpid()).ppid())== 1:
    #           #the script is run as a service, just exiting will restart it
    #           exit()
    
    
    # #otherwise use a system command and execv to restart the script 
    # print("restarting script...")
    # os.system("sudo systemctl restart grottserver.service")
    # os.execv(sys.argv[0], sys.argv)
    
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

print(os.getcwd())

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
