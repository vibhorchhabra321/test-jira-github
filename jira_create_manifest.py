import json

class service(dict):
 
  # __init__ function
  def __init__(self):
    self = dict()
 
  # Function to add key:value
  def add(self, key, value):
    self[key] = value
 
 
# Main Function
svc_obj = service()
main_manifest_json = service()
 
services = []
aList = ["svc-v1-lib","svc2-v2-lib", "svc3-v1-lib"]
for svc in aList:
    service_manifest=svc.split('-v')
    service_manifest[1]="v" + service_manifest[1][0:]
    svc_obj.add("Service_Name", service_manifest[0])
    svc_obj.add("Service_Version", service_manifest[1])
    services.append(svc_obj)
main_manifest_json.add("Services",services)
print(main_manifest_json)
#with open('main_manifest_json.json', 'w') as f:
#    json.dump(main_manifest_json, f, ensure_ascii=False, indent=4)
