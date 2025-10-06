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

    minimalDashboard = {"views":[{"title":"Grott Generated Dashboard","sections":[{"type":"grid", "cards":[{"type":"heading", "heading":"No Inverters detected yet"}]}]}]}
    
    dashboardConfig = {"views":[{"title":"Grott Generated Dashboard","sections":[{"type":"grid", "cards":[{"type":"heading", "heading":"No Inverters detected yet"}]}]}]}

    sensorNameTag = "sensor."+deviceid.lower()

    dashboardSections = dashboardConfig["views"][0]["sections"]

    newSection = {"type":"grid", "cards":[]}
    sectionHeader = {"type":"heading", "heading":deviceid}
    newSection["cards"].append(sectionHeader)
    pvInGauge = {"type":"gauge", "entity":sensorNameTag+"_pv_all_power", "name":"PV Eingangsleistung"}
    newSection["cards"].append(pvInGauge)
    bat01Gauge = {"type":"gauge", "entity":sensorNameTag+"_battery_1_soc", "name":"Ladestand Batterie 1"}
    newSection["cards"].append(pvInGauge)
    #dashboardSections.append(newSection)
    dashboardConfig["views"][0]["sections"][0]= newSection

    with open(locoWattYamlDashboardLocation, 'w') as outfile:
        yaml.dump(dashboardConfig, outfile)




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
