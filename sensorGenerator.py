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
def sensorListMaker(configDictionary, pvSerial):
    sensorList = []
    #print(configDictionary)
    for key in configDictionary:
        entry = configDictionary[key]
        #print(configDictionary[entry])
        #print(type(configDictionary[entry]))
        print(key)
        print(type(key))
        print(entry)
        print(type(entry))
        if (key != "decrypt") and (key != "date") and (key != "pvserial") and (key != "datalogserial"):
            try:
                if entry["incl"]=="no":
                    bShouldBeIncluded = False
                else:
                    bShouldBeIncluded = True
            except:
                bShouldBeIncluded = True

            if bShouldBeIncluded:
                bUnitentry = False
                try:
                    bUnitentry = True
                    entryUnit = entry["unit"]
                    print(entryUnit)
                except:
                    bUnitEntry = False
                
                if bUnitEntry:
                    if entryUnit=="V":
                        sensorUnit = "V"
                        sensorType = "voltage"
                    elif entryUnit=="W":
                        sensorUnit = "W"
                        sensorType = "power"
                    elif entryUnit=="kWh":
                        sensorUnit = "kWh"
                        sensorType = "energy"
                    elif entryUnit=="A":
                        sensorUnit = "A"
                        sensorType = "current"
                    elif entryUnit=="degC":
                        sensorUnit = "°C"
                        sensorType = "temperature"
                    elif entryUnit=="%":
                        sensorUnit = "%"
                        sensorType = "battery"
                    else:
                        print("no unit")
                        bHasUnit = False
                        sensorType = "power"
                    
                    if bHasUnit:
                        newSensor = {'sensor':{'name':key,'device_class': sensorType, 'unit_of_measurement':sensorUnit, 'unique_id':pvSerial+key, 'state_topic':'energy/growatt/'+pvSerial, 'value_template':'{{ float(value_json.data.'+key+')/'+ str(entry["divide"]) +' }}', 'device': {'identifiers': pvSerial, 'name': 'Growatt '+pvSerial}}}
                    else:
                        newSensor = {'sensor':{'name':key,'device_class': sensorType, 'unique_id':pvSerial+key, 'state_topic':'energy/growatt/'+pvSerial, 'value_template':'{{ float(value_json.data.'+key+')/'+ str(entry["divide"]) +' }}', 'device': {'identifiers': pvSerial, 'name': 'Growatt '+pvSerial}}}
                else:
                    newSensor = {'sensor':{'name':key, 'unique_id':pvSerial+key, 'state_topic':'energy/growatt/'+pvSerial, 'value_template':'{{ float(value_json.data.'+key+')/'+ str(entry["divide"]) +' }}', 'device': {'identifiers': pvSerial, 'name': 'Growatt '+pvSerial}}}
                
                sensorList.append(newSensor)
            #print(key, dictionary['data'][key])
    return sensorList


def writeSensorsToFile(sensorList, filePath):
    with open('testout4.yaml','w') as outfile:
        yaml.dump(sensorList,outfile)
        print("written sensors to "+filePath)

def updateSensors(configDictionary, filePath, pvSerial):
    print("checking if sensors need updating")
    bSensorsNeedUpdating = True
    if bSensorsNeedUpdating:
        print("updating sensors")
        print("for device: "+pvSerial)
        newSensorList = sensorListMaker(configDictionary, pvSerial)
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
