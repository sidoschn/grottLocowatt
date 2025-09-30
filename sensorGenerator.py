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

def sensorListMaker(dictionary):
    sensorList = []
    for key in dictionary['data']:
        newSensor = {'sensor':{'name':key, 'unique_id':dictionary['device']+key, 'state_topic':'energy/growatt', 'value_template':'{{ value_json.data.'+key+' }}', 'device': {'identifiers': dictionary['device'], 'name': 'Growatt '+dictionary['device']}}}
        sensorList.append(newSensor)
        #print(key, dictionary['data'][key])
    return sensorList


def updateSensors(configDictionary):
    print("checking if sensors need updating")
    bSensorsNeedUpdating = True
    if bSensorsNeedUpdating:
        print("updating sensors")
        for entry in configDictionary:
            print(entry)


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
