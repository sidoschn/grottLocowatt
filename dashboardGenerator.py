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
        minimalDashboard = {"views":[{"title":"Grott Generated Dashboard","sections":[{"type":"grid", "cards":[{"type":"heading", "heading":"No Inverters detected yet"}]}]}]}
        
        dashboardConfig = {"views":[{"title":"Solar Dashboard","sections":[{"type":"grid", "cards":[{"type":"heading", "heading":"No Inverters detected yet"}]}]}]}

        sensorNameTag = "sensor.growatt_"+deviceid.lower()+"_"

        dashboardSections = dashboardConfig["views"][0]["sections"]

        newSection = {"type":"grid", "cards":[]}
        sectionHeader = {"type":"heading", "heading":deviceid}
        newSection["cards"].append(sectionHeader)
        lastUpdate= {"type":"heading", "heading": "Last Update:", "badges":[{"type":"entity","entity":sensorNameTag+"last_update"}]}
        newSection["cards"].append(lastUpdate)
        pvInGauge = {"type":"gauge", "entity":sensorNameTag+"pvpowerin", "name":"PV Eingangsleistung", "max":definedkey["opfullwatt"]}
        newSection["cards"].append(pvInGauge)
        bat01Gauge = {"type":"gauge", "entity":sensorNameTag+"bdc1_soc", "name":"Ladestand Batterie 1"}
        newSection["cards"].append(bat01Gauge)
        #dashboardSections.append(newSection)
        dashboardConfig["views"][0]["sections"][0]= newSection

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
