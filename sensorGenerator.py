import yaml
import os

locoWattYamlSensorsLocation = "/home/admin/HA/config/mqttSensors.yaml"


def keyPrinter(dictionary):
    for key in dictionary:
        if type(dictionary[key]) == dict:
            keyPrinter(dictionary[key])
        else:
            print(key, dictionary[key])
        
# def sensorListMaker(dictionary, fulldict):
#     sensorList = []
#     for key in dictionary:
#             if type(dictionary[key]) == dict:
#                 subSensorList = sensorListMaker(dictionary[key], fulldict)
#                 for key in subSensorList:
#                     sensorList.append(subSensorList[key])
#             else:
#                 newSensor = {'sensor':{'name':key, 'unique_id':fulldict['device']}}
#                 sensorList.append(newSensor)
#                 print(key, dictionary[key])
#     return sensorList

#make a new sensor list from a config dictionary
def sensorListMaker(configDictionary, pvSerial, jsondate):
    sensorList = []
    #print(configDictionary)
    for key in configDictionary:
        entry = configDictionary[key]
        #print(configDictionary[entry])
        #print(type(configDictionary[entry]))
        # print(key)
        # print(type(key))
        # print(entry)
        # print(type(entry))
        
        # always add a new sensor that displays the timestamp received sent from grott through MQTT
        newSensor = {'sensor':{'name':'last Update', 'unique_id': pvSerial+"lastUpdate", 'state_topic':'energy/growatt/'+pvSerial, 'value_template':'{{ value_json.time | as_datetime }}', 'device': {'identifiers': pvSerial, 'name': 'Growatt '+pvSerial}}}
        sensorList.append(newSensor)
        
        if (key != "decrypt") and (key != "date") and (key != "pvserial") and (key != "datalogserial"):
            try:
                if entry["incl"]=="no":
                    bShouldBeIncluded = False
                else:
                    bShouldBeIncluded = True
            except:
                bShouldBeIncluded = True

            if bShouldBeIncluded:
                bUnitEntry = False
                try:
                    bUnitEntry = True
                    entryUnit = entry["unit"]
                    #print(entryUnit)
                except:
                    bUnitEntry = False
                
                bHasUnit = True
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
                        #print("no unit")
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
    with open(filePath,'w') as outfile:
        yaml.dump(sensorList,outfile)
        print("sensor update written sensors to "+ filePath)

def updateSensors(configDictionary, pvSerial, deviceid, jsondate):
    print("checking if sensors need updating")
    
    if deviceid==pvSerial:
        bSensorsNeedUpdating = True
    else:
        bSensorsNeedUpdating = False

    if bSensorsNeedUpdating:
        print("updating sensors")
        print("for device: "+deviceid)
        newSensorList = sensorListMaker(configDictionary, deviceid, jsondate)
        writeSensorsToFile(newSensorList, locoWattYamlSensorsLocation)



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
