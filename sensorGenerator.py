import yaml
import os

def keyPrinter(dictionary):
    for key in dictionary:
        if type(dictionary[key]) == dict:
            keyPrinter(dictionary[key])
        else:
            print(key, dictionary[key])
        
def sensorListMaker(dictionary, fulldict):
    sensorList = []
    for key in dictionary:
            if type(dictionary[key]) == dict:
                subSensorList = sensorListMaker(dictionary[key], fulldict)
                for key in subSensorList:
                    sensorList.append(subSensorList[key])
            else:
                newSensor = {'sensor':{'name':key, 'unique_id':fulldict['device']}}
                sensorList.append(newSensor)
                print(key, dictionary[key])
    return sensorList

#make a new sensor list from a config dictionary
def sensorListMaker(configDictionary):
    sensorList = []
    for entry in configDictionary:
        try:
            if entry["incl"]=="no":
                bShouldBeIncluded = False
            else:
                bShouldBeIncluded = True
        except:
            bShouldBeIncluded = True

        if bShouldBeIncluded:
            try:
                bUnitentry = True
                match entry["unit"]:
                    case "V":
                        sensorUnit = "V"
                        sensorType = "voltage"
                    case "W":
                        sensorUnit = "W"
                        sensorType = "power"
                    case "kWh":
                        sensorUnit = "kWh"
                        sensorType = "energy"
                    case "W":
                        sensorUnit = "W"
                        sensorType = "power"
                    case "A":
                        sensorUnit = "A"
                        sensorType = "current"
                    case "degC":
                        sensorUnit = "°C"
                        sensorType = "temperature"
                    case "%":
                        sensorUnit = "%"
                        sensorType = "battery"
                    case _:
                        print("no unit")
                        bUnitEntry = False
                        sensorType = "power"
                
                if bUnitEntry:
                    newSensor = {'sensor':{'name':entry,'device_class': sensorType, 'unit_of_measurement':sensorUnit, 'unique_id':configDictionary['device']+entry, 'state_topic':'energy/growatt', 'value_template':'{{ value_json.data.'+entry+'/'+ entry["divide"] +' }}', 'device': {'identifiers': configDictionary['device'], 'name': 'Growatt '+configDictionary['device']}}}
                else:
                    newSensor = {'sensor':{'name':entry,'device_class': sensorType, 'unique_id':configDictionary['device']+entry, 'state_topic':'energy/growatt', 'value_template':'{{ value_json.data.'+entry+'/'+ entry["divide"] +' }}', 'device': {'identifiers': configDictionary['device'], 'name': 'Growatt '+configDictionary['device']}}}
            except:
                newSensor = {'sensor':{'name':entry, 'unique_id':configDictionary['device']+entry, 'state_topic':'energy/growatt', 'value_template':'{{ value_json.data.'+entry+'/'+ entry["divide"] +' }}', 'device': {'identifiers': configDictionary['device'], 'name': 'Growatt '+configDictionary['device']}}}
            sensorList.append(newSensor)
            #print(key, dictionary['data'][key])
    return sensorList


def writeSensorsToFile(sensorList, filePath):
    with open('testout4.yaml','w') as outfile:
        yaml.dump(sensorList,outfile)
        print("written sensors to "+outfile)

def updateSensors(configDictionary, filePath):
    print("checking if sensors need updating")
    bSensorsNeedUpdating = True
    if bSensorsNeedUpdating:
        print("updating sensors")
        newSensorList = sensorListMaker(configDictionary)
        writeSensorsToFile(newSensorList, filePath)



# def writeSensorYaml(sensorList, outFile)
#     with open(outFile, 'w') as outputFile:
#         yaml.dump(sensorList, outputFile)


def checkSensors(yamlFilePath):
    print(os.path.isfile(yamlFilePath))
    return 

def getSensors(yamlFilePath):
    if os.path.isfile(yamlFilePath):
        with open(yamlFilePath) as fileStream:
            readSensorList = yaml.safe_load(fileStream)
    else:
        readSensorList = []
    return readSensorList

def getListOfDevicesFromSensorList(sensorList):
    listOfDevices = []

    for listEntry in sensorList:
        if not listEntry['sensor']['device']['identifiers'] in listOfDevices:
            listOfDevices.append(listEntry['sensor']['device']['identifiers'])
    
    return listOfDevices
        




        



#asf = eval(open('growattOutputExample(MIN).yaml', 'r').read())

#ownDict = {"asf" : "klkjlk", "lllkk": "iririri"}

#print(ownDict)
#print(asf["data"]["pvstatus"])

#print(type(asf))
#print(asf["data"].keys())

#keyPrinter(asf)

#bb = [{'sensor':{'name':'asdf', 'device':'gggg'}},{'sensor':{'name':'asd2f', 'device':'gggg2'}}]


#af = sensorListMaker(asf)

#with open('testout.yaml', 'w') as outfile:
#    yaml.dump(af, outfile)


#print('done')
