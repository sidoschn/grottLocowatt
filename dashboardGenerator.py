# generates dashboards for HomeAssistant
import yaml

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


def generateDashboard(definedkey, deviceid, jsondate):
    try:
        #minimalDashboard = {"views":[{"title":"Grott Generated Dashboard","sections":[{"type":"grid", "cards":[{"type":"heading", "heading":"No Inverters detected yet"}]}]}]}
        
        dashboardConfig = {"views":[{"title":"Solar Dashboard","sections":[{"type":"grid", "cards":[{"type":"heading", "heading":"No Inverters detected yet"}]}]}]}

        sensorNameTag = "sensor.growatt_"+deviceid.lower()+"_"

        # initialize new section
        newSection = {"type":"grid", "cards":[]}
        
        #additional sensors needed:
        #grid import export sensor (with +-)
        #battery charge sensor (with +-)

        #fill the new section with cards
        newSection["cards"].append({"type":"heading", "heading":deviceid}) #heading of the section
        newSection["cards"].append({"type":"heading", "heading": "Last Update:", "badges":[{"type":"entity","entity":sensorNameTag+"last_update"}]}) #time of last update (in header)
        newSection["cards"].append({"type":"gauge", "entity":sensorNameTag+"pvpowerin", "name":"PV Eingangsleistung", "grid_options":{"columns":6,"rows":"auto"}, "max":definedkey["opfullwatt"]}) #total input of PV panels
        newSection["cards"].append({"type":"gauge", "entity":sensorNameTag+"pvpowerout", "name":"Inverter Ausgangsleistung", "grid_options":{"columns":6,"rows":"auto"}, "max":definedkey["opfullwatt"]}) #total output of inverter
        newSection["cards"].append({"type":"gauge", "entity":sensorNameTag+"ptoloadtotal", "name":"Eigenverbrauch", "grid_options":{"columns":6,"rows":"auto"}, "max":definedkey["opfullwatt"]}) #total self conumed power
        newSection["cards"].append({"type":"gauge", "entity":sensorNameTag+"pgridimportexport", "name":"Netz Exportleistung", "grid_options":{"columns":6,"rows":"auto"}, "severity":{"green":0,"yellow":-definedkey["opfullwatt"],"red":(-definedkey["opfullwatt"]-10)}, "max":definedkey["opfullwatt"], "min":-definedkey["opfullwatt"], "needle":"true"}) #power exported to grid
        newSection["cards"].append({"type":"gauge", "entity":sensorNameTag+"pbdc1chrdischr", "name":"Batterie 1 Ladeleistung", "grid_options":{"columns":6,"rows":"auto"}, "severity":{"green":0,"yellow":-definedkey["opfullwatt"],"red":(-definedkey["opfullwatt"]-10)}, "max":(definedkey["opfullwatt"]/2), "min":-(definedkey["opfullwatt"]/2), "needle":"true"}) #power exported to grid
        newSection["cards"].append({"type":"gauge", "entity":sensorNameTag+"pbdc2chrdischr", "name":"Batterie 2 Ladeleistung", "grid_options":{"columns":6,"rows":"auto"}, "severity":{"green":0,"yellow":-definedkey["opfullwatt"],"red":(-definedkey["opfullwatt"]-10)}, "max":(definedkey["opfullwatt"]/2), "min":-(definedkey["opfullwatt"]/2), "needle":"true"}) #power exported to grid
        #newSection["cards"].append({"type":"gauge", "entity":sensorNameTag+"ptousertotal", "name":"Netz Importleistung", "grid_options":{"columns":6,"rows":"auto"}, "max":definedkey["opfullwatt"]}) #power imported from grid
        #newSection["cards"].append({"type":"gauge", "entity":sensorNameTag+"ptousertotal", "name":"Netz Importleistung", "grid_options":{"columns":6,"rows":"auto"}, "max":definedkey["opfullwatt"]}) #power imported from grid

        newSection["cards"].append({"type":"gauge", "entity":sensorNameTag+"bdc1_soc", "name":"Ladestand Batterie 1", "severity":{"green":50,"yellow":15,"red":0}, "grid_options":{"columns":6,"rows":"auto"}})
        newSection["cards"].append({"type":"gauge", "entity":sensorNameTag+"bdc2_soc", "name":"Ladestand Batterie 2", "severity":{"green":50,"yellow":15,"red":0}, "grid_options":{"columns":6,"rows":"auto"}})
        
        
        
        
        # add new section to dashboard
        dashboardConfig["views"][0]["sections"][0]= newSection
        
        print(dashboardConfig)

        with open(locoWattYamlDashboardLocation, 'w') as outfile:
            yaml.dump(dashboardConfig, outfile)
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
