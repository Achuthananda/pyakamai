import requests,json
from akamaihttp import AkamaiHTTPHandler
from getcpcodes import fetchCPCodes

accountSwitchKey = 'F-AassaC-1asdasdasd526355:1-2RBL' 

#Fetch the Configs and CP Codes
configList = open('configlist.txt','r').readlines()
configList = [x.strip('\n') for x in configList]

cpcodeList = []
def fetchCPCodes():
	for config in configList:
		print(config)
		myconfig = AkamaiProperty(edgercLocation,config,accountSwitchKey)
		for x in myconfig.getCPCodes(myconfig.getStagingVersion()):
			cpcodeList.append(x)


#Prepare the payload for Event Creation
payload = {
    "objects": [],
    "description": "Test Event",
    "name": "Test Event3",
    "start": "2022-08-01T08:00:00Z",
    "end": "2022-08-03T20:00:00Z",
}
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

for cpCode in configList:
    newobj = {}
    newobj['type'] = 'CP_CODE'
    newobj['id'] = cpCode
    payload['objects'].append(newobj)

eventobj_json = json.dumps(payload)

#Call the API to Create the Event
akhttp = AkamaiHTTPHandler('/Users/apadmana/.edgerc')
ep = "/events/v3/events"
params = {}
params['accountSwitchKey'] = accountSwitchKey

status,eventcreateJson = akhttp.postResult(ep,eventobj_json,headers=headers,params=params)
if status != 200:
    print(json.dumps(eventcreateJson,indent=2))


print("Control Room Link:",'https://control.akamai.com/apps/event-center/#/schedule/events/{}/control-room'.format(str(eventcreateJson[0]['id'])))





