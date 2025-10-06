# generates dashboards for HomeAssistant
import yaml

def debugPrintout(definedkey, deviceid, jsondate):
    print("--- debugout:")
    print(definedkey)
    print("device ID:")
    print(deviceid)
    print(jsondate)
    print("--- end debugout")


def generateDashboard(definedkey, deviceid, jsondate):
    minimalDashboard = {"views":[{"title":"Grott Generated Dashboard","sections":[{"type":"heading", "heading":"deviceId"}, {"type":"gauge", "entity":"sensorID"}]}]}
    
    with open('/home/admin/HA/config/grottDashboardConfig.yaml', 'w') as outfile:
        yaml.dump(minimalDashboard, outfile)


# views:
# - sections:
#   - heading: deviceId
#     type: heading
#   - entity: sensorID
#     type: gauge
#   title: title
