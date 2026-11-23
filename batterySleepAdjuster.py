# this script remembers and returns the last known SOC of a battery to suppress confusing energy readings if a bdc disconnects 

import configparser
import os

memoryFileName = "socMemory.ini"
defaultConfig = configparser.ConfigParser()
bdc1Section = "bdc1"
bdc2Section = "bdc2"

def initMemoryFile(fileName):
    print("generating new memory file from defaults")

    defaultConfig[bdc1Section] = {}
    defaultConfig[bdc1Section]["everConnected"] = "no"
    defaultConfig[bdc1Section]["SoC"] = str(0)
    
    defaultConfig[bdc2Section] = {}
    defaultConfig[bdc2Section]["everConnected"] = "no"
    defaultConfig[bdc2Section]["SoC"] = str(0)

    with open(memoryFileName, 'w') as configFile:
        defaultConfig.write(configFile)

    return defaultConfig
    #memoryDict = {"bdc1EverConnected":False,"bdc1SoC":0, "bdc1ConnectionState":False,"bdc2EverConnected":False,"bdc2SoC":0, "bdc2ConnectionState":False}


def adjustForBatterySleep(definedkey):

    memoryData = loadMemoryFile()
    newMemory = memoryData

    # checking for battery connection states
    # bcdonoffstates: 0=no battery, 1 = battery1 connected, 2 = battery2 connected, 3 = battery1 and battery2 connected
    if (definedkey["bdconoffstate"] == 1):
        # battery 1 is connected
        newMemory = memorizeBatterySoC(definedkey, 1, newMemory)
        if memoryData[bdc2Section]["everConnected"]=="yes":
            recallBatterySoC(definedkey, 2, memoryData)
    elif(definedkey["bdconoffstate"] == 2):
        # battery 2 is connected
        newMemory= memorizeBatterySoC(definedkey, 2, newMemory)
        if memoryData[bdc1Section]["everConnected"]=="yes":
            recallBatterySoC(definedkey, 1, memoryData)
    elif (definedkey["bdconoffstate"] == 3):
        # battery 1 and 2 are connected
        newMemory = memorizeBatterySoC(definedkey, 1, newMemory)
        newMemory = memorizeBatterySoC(definedkey, 2, newMemory)
    else:
        recallBatterySoC(definedkey, 1, memoryData)
        recallBatterySoC(definedkey, 2, memoryData)

    if newMemory!=memoryData:
        print("SoC values adjusted for sleeping Battery")
        saveMemoryFile(newMemory)
    else:
        print("No sleep SoC value adjustment needed")

def memorizeBatterySoC(definedkey, batteryIndex, memoryData):
    #save SOC to file for later use
    if batteryIndex == 1:
        bdcSoC = definedkey["bdc1_soc"]
        memoryData[bdc1Section]["everConnected"] = "yes"
        memoryData[bdc1Section]["SoC"] = str(bdcSoC)
    elif batteryIndex == 2:
        bdcSoC = definedkey["bdc2_soc"]
        memoryData[bdc2Section]["everConnected"] = "yes"
        memoryData[bdc2Section]["SoC"] = str(bdcSoC)

    return memoryData




def recallBatterySoC(definedkey, bdcIdx, memoryData):
    #recall batterySoCs
    memoryData = loadMemoryFile()

    if bdcIdx == 1:
        definedkey["bdc1_soc"] = int(memoryData[bdc1Section]["SoC"])
    elif bdcIdx == 2:
        definedkey["bdc2_soc"] = int(memoryData[bdc2Section]["SoC"])

    #print("recalling Battery SoC")


def saveMemoryFile(memoryData):
    with open(memoryFileName, 'w') as memoryFile:
      memoryData.write(memoryFile)


def loadMemoryFile():
    if not os.path.isfile(memoryFileName):
        memoryData = initMemoryFile(memoryFileName)
    else:
        #print("reading config from file: "+ self.configFileName)
        memoryData = configparser.ConfigParser()
        memoryData.read(memoryFileName)

    return memoryData