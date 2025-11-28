# generates dashboards for HomeAssistant
import yaml
import os

locoWattYamlDashboardLocation = '/home/admin/HA/config/grottDashboardConfig.yaml'


def debugPrintout(definedkey, deviceid, jsondate):
    print("--- debugout:")
    print(definedkey)
    print("device ID:")
    print(deviceid)
    print(jsondate)
    print("--- end debugout")


def generateMinimalDashboard(definedkey, deviceid, jsondate):
    minimalDashboard = {"views":[{"title":"Grott Generated Dashboard","sections":[{"type":"grid", "cards":[{"type":"heading", "heading":"No Inverters detected yet"}]}]}]}
    
    with open(locoWattYamlDashboardLocation, 'w') as outfile:
        yaml.dump(minimalDashboard, outfile)


def generateDashboard(definedkey, deviceid, jsondate, recordlayout, rRCRcontrollers):
    bFirstrun = False
    if not os.path.isfile(locoWattYamlDashboardLocation):
        print("first run conditions detected!")
        bFirstrun = True


    try:
        #minimalDashboard = {"views":[{"title":"Grott Generated Dashboard","sections":[{"type":"grid", "cards":[{"type":"heading", "heading":"No Inverters detected yet"}]}]}]}
        
        dashboardConfig = {"views":[{"title":"Solar Dashboard","sections":[{"type":"grid", "cards":[{"type":"heading", "heading":"No Inverters detected yet"}]}]}]}

        sensorNameTag = "sensor.growatt_"+deviceid.lower()+"_"
        binSensorNameTag = "binary_sensor.growatt_"+deviceid.lower()+"_"

        # initialize new section
        newSection = {"type":"grid", "cards":[], "badges":[]}
        
        #additional sensors needed:
        #grid import export sensor (with +-)
        #battery charge sensor (with +-)
        maximumSystemPower = (definedkey["opfullwatt"]/recordlayout["opfullwatt"]["divide"])
        #fill the new section with cards
        # power related cards: 
        newSection["cards"].append({"type":"heading", "heading":deviceid}) #heading of the section
        newSection["cards"].append({"type":"heading", "heading": "Letztes Update:", "badges":[{"type":"entity","entity":sensorNameTag+"last_update"}]}) #time of last update (in header)
        newSection["cards"].append({"type":"gauge", "entity":sensorNameTag+"pvpowerin", "name":"PV Eingangsleistung", "grid_options":{"columns":6,"rows":"auto"}, "max":maximumSystemPower}) #total input of PV panels
        newSection["cards"].append({"type":"gauge", "entity":sensorNameTag+"pvpowerout", "name":"Inverter Ausgangsleistung", "grid_options":{"columns":6,"rows":"auto"}, "max":maximumSystemPower}) #total output of inverter
        newSection["cards"].append({"type":"gauge", "entity":sensorNameTag+"ptoloadtotal", "name":"Eigenverbrauch", "grid_options":{"columns":6,"rows":"auto"}, "max":maximumSystemPower}) #total self conumed power
        newSection["cards"].append({"type":"gauge", "entity":sensorNameTag+"pgridimportexport", "name":"Netz Exportleistung", "grid_options":{"columns":6,"rows":"auto"}, "severity":{"green":0,"yellow":-maximumSystemPower,"red":(-maximumSystemPower-10)}, "max":maximumSystemPower, "min":-maximumSystemPower, "needle":"true"}) #power exported to grid
        
        # battery related cards:
        # checking for battery states before displaying the battery cards
        # bcdonoffstates: 0=no battery, 1 = battery1 connected, 2 = battery2 connected, 3 = battery1 and battery2 connected
              
        if (definedkey["bdconoffstate"] == 1 or definedkey["bdconoffstate"] == 3): 
            newSection["cards"].append({"type":"gauge", "entity":sensorNameTag+"pbdc1chrdischr", "name":"Batterie 1 Ladeleistung", "grid_options":{"columns":6,"rows":"auto"}, "severity":{"green":0,"yellow":-maximumSystemPower,"red":(-maximumSystemPower-10)}, "max":(8000), "min":-(8000), "needle":"true"}) #power exported to grid
        
        if (definedkey["bdconoffstate"] > 1): 
            newSection["cards"].append({"type":"gauge", "entity":sensorNameTag+"pbdc2chrdischr", "name":"Batterie 2 Ladeleistung", "grid_options":{"columns":6,"rows":"auto"}, "severity":{"green":0,"yellow":-maximumSystemPower,"red":(-maximumSystemPower-10)}, "max":(8000), "min":-(8000), "needle":"true"}) #power exported to grid
        
        if (definedkey["bdconoffstate"] == 1 or definedkey["bdconoffstate"] == 3): 
            newSection["cards"].append({"type":"gauge", "entity":sensorNameTag+"bdc1_soc", "name":"Ladestand Batterie 1", "severity":{"green":50,"yellow":15,"red":0}, "grid_options":{"columns":6,"rows":"auto"}})
        
        if (definedkey["bdconoffstate"] > 1): 
            newSection["cards"].append({"type":"gauge", "entity":sensorNameTag+"bdc2_soc", "name":"Ladestand Batterie 2", "severity":{"green":50,"yellow":15,"red":0}, "grid_options":{"columns":6,"rows":"auto"}})


        # history graph cards

        # -- system power overview
        entitiesToAdd =[]
        entitiesToAdd.append({"entity":sensorNameTag+"pvpowerin", "name":"PV Eingang"})
        entitiesToAdd.append({"entity":sensorNameTag+"pvpowerout", "name":"Inverter Ausgang"})
        entitiesToAdd.append({"entity":sensorNameTag+"ptoloadtotal", "name":"Eigenverbrauch"})
        entitiesToAdd.append({"entity":sensorNameTag+"ptogridtotal", "name":"Netz Export"})
        entitiesToAdd.append({"entity":sensorNameTag+"ptousertotal", "name":"Netz Import"})
        
        if (definedkey["bdconoffstate"] == 1 or definedkey["bdconoffstate"] == 3): 
            entitiesToAdd.append({"entity":sensorNameTag+"bdc1_pchr", "name":"Batterie 1 Ladung"})
            entitiesToAdd.append({"entity":sensorNameTag+"bdc1_pdischr", "name":"Batterie 1 Entladung"})
        
        if (definedkey["bdconoffstate"] > 1): 
            entitiesToAdd.append({"entity":sensorNameTag+"bdc2_pchr", "name":"Batterie 2 Ladung"})
            entitiesToAdd.append({"entity":sensorNameTag+"bdc2_pdischr", "name":"Batterie 2 Entladung"})
        
        newSection["cards"].append({"type":"history-graph", "title":"Anlagenleistung Übersicht", "entities":entitiesToAdd, "name":"Anlagenleistung Übersicht", "hours_to_show" : 48, "grid_options":{"columns":13,"rows":6}})

        # -- pv MPPT powers

        entitiesToAdd =[]
        for i in range(10):
            try:
                entitiesToAdd.append({"entity":sensorNameTag+"pv"+str(i)+"watt", "name":"Tracker " + str(i)})
            except:
                asdf = 1

        newSection["cards"].append({"type":"history-graph", "title":"PV Tracker Leistungen", "entities":entitiesToAdd, "name":"PV Tracker Leistungen", "hours_to_show" : 48, "grid_options":{"columns":13,"rows":4}})
        
        # -- pv MPPT voltages

        entitiesToAdd =[]
        for i in range(10):
            try:
                entitiesToAdd.append({"entity":sensorNameTag+"pv"+str(i)+"voltage", "name":"Tracker " + str(i)})
            except:
                asdf = 1

        newSection["cards"].append({"type":"history-graph", "title":"PV Tracker Spannungen", "entities":entitiesToAdd, "name":"PV Tracker Spannungen", "hours_to_show" : 48, "grid_options":{"columns":13,"rows":4}})
        
        # -- pv MPPT currents

        entitiesToAdd =[]
        for i in range(10):
            try:
                entitiesToAdd.append({"entity":sensorNameTag+"pv"+str(i)+"current", "name":"Tracker " + str(i)})
            except:
                asdf = 1

        newSection["cards"].append({"type":"history-graph", "title":"PV Tracker Stromstärken", "entities":entitiesToAdd, "name":"PV Tracker Stromstärken", "hours_to_show" : 48, "grid_options":{"columns":13,"rows":4}})

        entitiesToAdd =[]
        for controller in rRCRcontrollers:
            i = 1
            try:
                entitiesToAdd.append({"entity":binSensorNameTag+controller.attachedToLogger.lower()+"isrrcractive", "name":"RRCR Controller " + str(i)})
            except:
                asdf = 1
            i = i + 1

        
        newSection["cards"].append({"type":"history-graph", "title":"Rundsteuerempfänger Status", "entities": entitiesToAdd, "name":"Rundsteuerempfänger Status", "hours_to_show" : 48, "grid_options":{"columns":13,"rows":2}})
            #newSection["cards"].append({"type":"history-graph", "title":"PV Tracker Stromstärken", "entities":entitiesToAdd, "name":"PV Tracker Stromstärken", "hours_to_show" : 48, "grid_options":{"columns":13,"rows":4}})
        
        
        
        # add new section to dashboard
        dashboardConfig["views"][0]["sections"][0]= newSection
        
        with open(locoWattYamlDashboardLocation, 'w') as outfile:
            yaml.dump(dashboardConfig, outfile)
            print("Dashboard update written to "+locoWattYamlDashboardLocation)

        if bFirstrun:
            
            os.system("sudo docker restart homeassistant")

    except:
        print("unable to generate dashboard")




# views:
# - sections:
#   - heading: deviceId
#     type: heading
#   - entity: sensorID
#     type: gauge
#   title: title

# views:
#   - title: Home
#     sections:
#       - type: grid
#         cards:
#           - type: heading
#             heading: Section 01
#             heading_style: title
#           - type: gauge
#             entity: sensor.dlp0dyt037_battery_1_soc
#             name: gauge 01
