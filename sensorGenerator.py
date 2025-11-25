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
def sensorListMaker(configDictionary, pvSerial, jsondate, rRCRcontrollers):
    sensorList = []
    #print(configDictionary)

    # always add a new sensor that displays the timestamp received sent from grott through MQTT
    newSensor = {'sensor':{'name':'last Update', 'unique_id': pvSerial+"lastUpdate", 'state_topic':'energy/growatt/'+pvSerial, 'value_template':'{{ value_json.time | as_datetime }}', 'device': {'identifiers': pvSerial, 'name': 'Growatt '+pvSerial}}}
    sensorList.append(newSensor)

    # add sensors according to the applied config dictionary for the device
    for key in configDictionary:
        entry = configDictionary[key]
        
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
                        stateClass = "measurement"
                    elif entryUnit=="W":
                        sensorUnit = "W"
                        sensorType = "power"
                        stateClass = "measurement"
                    elif entryUnit=="kWh":
                        sensorUnit = "kWh"
                        sensorType = "energy"
                        stateClass = "total"
                    elif entryUnit=="A":
                        sensorUnit = "A"
                        sensorType = "current"
                        stateClass = "measurement"
                    elif entryUnit=="degC":
                        sensorUnit = "°C"
                        sensorType = "temperature"
                        stateClass = "measurement"
                    elif entryUnit=="%":
                        sensorUnit = "%"
                        sensorType = "battery"
                        stateClass = "measurement"
                    else:
                        #print("no unit")
                        bHasUnit = False
                        sensorType = "power"
                    
                    if bHasUnit:
                        newSensor = {'sensor':{'name':key,'device_class': sensorType, 'unit_of_measurement':sensorUnit, 'unique_id':pvSerial+key, 'state_class':stateClass, 'state_topic':'energy/growatt/'+pvSerial, 'value_template':'{{ float(value_json.data.'+key+')/'+ str(entry["divide"]) +' }}', 'device': {'identifiers': pvSerial, 'name': 'Growatt '+pvSerial}}}
                    else:
                        newSensor = {'sensor':{'name':key,'device_class': sensorType, 'unique_id':pvSerial+key, 'state_class':stateClass, 'state_topic':'energy/growatt/'+pvSerial, 'value_template':'{{ float(value_json.data.'+key+')/'+ str(entry["divide"]) +' }}', 'device': {'identifiers': pvSerial, 'name': 'Growatt '+pvSerial}}}
                else:
                    newSensor = {'sensor':{'name':key, 'unique_id':pvSerial+key, 'state_topic':'energy/growatt/'+pvSerial, 'value_template':'{{ float(value_json.data.'+key+')/'+ str(entry["divide"]) +' }}', 'device': {'identifiers': pvSerial, 'name': 'Growatt '+pvSerial}}}
                
                sensorList.append(newSensor)
            #print(key, dictionary['data'][key])
    
    # add custom and composit sensors here:

    # add sensors for RRCR controllers here:
    for controller in rRCRcontrollers:
        sensorUnit = "%"
        sensorType = "battery"
        stateClass = "measurement"
        newSensor = {'sensor':{'name':"exportLimitPercent",'device_class': sensorType, 'unit_of_measurement':sensorUnit, 'unique_id':pvSerial+"exportLimitPercent",'state_class':stateClass, 'state_topic':'energy/growatt/'+pvSerial, 'value_template':'{{ float(value_json.data.RRCRat'+controller.attachedToLogger+'Limit) }}', 'device': {'identifiers': pvSerial, 'name': 'Growatt '+pvSerial}}}
        sensorList.append(newSensor)

        #sensorType = "power"
        #newSensor = {'sensor':{'name':"isRRCRactive",'device_class': sensorType, 'unique_id':pvSerial+"isRRCRactive", 'state_class':stateClass, 'state_topic':'energy/growatt/'+pvSerial, 'value_template':'{{ (value_json.data.RRCRat'+controller.attachedToLogger+'Connected) }}', 'device': {'identifiers': pvSerial, 'name': 'Growatt '+pvSerial}}}
        newSensor = {'sensor':{'name':"isRRCRactive", 'unique_id':pvSerial+"isRRCRactive", 'state_class':stateClass, 'state_topic':'energy/growatt/'+pvSerial, 'value_template':'{{ (value_json.data.RRCRat'+controller.attachedToLogger+'Connected) }}', 'device': {'identifiers': pvSerial, 'name': 'Growatt '+pvSerial}}}
        sensorList.append(newSensor)


    # add power import-export sensor with + for export and - for import
    if ("ptogridtotal" in configDictionary and "ptousertotal" in configDictionary):
        #print(configDictionary["ptogridtotal"])
        sensorUnit = "W"
        sensorType = "power"
        newSensor = {'sensor':{'name':"pgridimportexport",'device_class': sensorType, 'unit_of_measurement':sensorUnit, 'unique_id':pvSerial+"pgridimportexport", 'state_topic':'energy/growatt/'+pvSerial, 'value_template':'{{ float(value_json.data.ptogridtotal-value_json.data.ptousertotal)/'+ str(configDictionary["ptogridtotal"]["divide"]) +' }}', 'device': {'identifiers': pvSerial, 'name': 'Growatt '+pvSerial}}}
        sensorList.append(newSensor)

    # add charge-discharge sensor for battery 1
    if ("bdc1_pchr" in configDictionary and "bdc1_pdischr" in configDictionary):
        #print(configDictionary["ptogridtotal"])
        sensorUnit = "W"
        sensorType = "power"
        newSensor = {'sensor':{'name':"pbdc1chrdischr",'device_class': sensorType, 'unit_of_measurement':sensorUnit, 'unique_id':pvSerial+"pbdc1chrdischr", 'state_topic':'energy/growatt/'+pvSerial, 'value_template':'{{ float(value_json.data.bdc1_pchr - value_json.data.bdc1_pdischr)/'+ str(configDictionary["bdc1_pchr"]["divide"]) +' }}', 'device': {'identifiers': pvSerial, 'name': 'Growatt '+pvSerial}}}
        sensorList.append(newSensor)

    # add charge-discharge sensor for battery 2
    if ("bdc2_pchr" in configDictionary and "bdc2_pdischr" in configDictionary):
        #print(configDictionary["ptogridtotal"])
        sensorUnit = "W"
        sensorType = "power"
        newSensor = {'sensor':{'name':"pbdc2chrdischr",'device_class': sensorType, 'unit_of_measurement':sensorUnit, 'unique_id':pvSerial+"pbdc2chrdischr", 'state_topic':'energy/growatt/'+pvSerial, 'value_template':'{{ float(value_json.data.bdc2_pchr - value_json.data.bdc2_pdischr)/'+ str(configDictionary["bdc2_pchr"]["divide"]) +' }}', 'device': {'identifiers': pvSerial, 'name': 'Growatt '+pvSerial}}}
        sensorList.append(newSensor)

    return sensorList


def writeSensorsToFile(sensorList, filePath):
    with open(filePath,'w') as outfile:
        yaml.dump(sensorList,outfile)
        print("sensor update written sensors to "+ filePath)

def updateSensors(configDictionary, pvSerial, deviceid, jsondate, rRCRcontrollers):
    print("checking if sensors need updating")
    
    if deviceid==pvSerial:
        bSensorsNeedUpdating = True
    else:
        bSensorsNeedUpdating = False

    if bSensorsNeedUpdating:
        print("updating sensors")
        print("for device: "+deviceid)
        newSensorList = sensorListMaker(configDictionary, deviceid, jsondate, rRCRcontrollers)
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
