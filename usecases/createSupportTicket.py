import requests,json
from akamaihttp import AkamaiHTTPHandler
import time,json
from ciscosparkapi import CiscoSparkAPI
from akamaiproperty import AkamaiProperty,AkamaiPropertyManager
import configparser
from pyakamai import pyakamai

accountSwitchKey = 'xyz'

edgercLocation = '/Users/apadmana/.edgerc'
akhttp = AkamaiHTTPHandler(edgercLocation)

config = configparser.ConfigParser()
config.read('config.ini')
print(config)


accessTokenDict = {
    "EteranadasdoSpace": 'dasda',
    "EterassssnoCustomerSpace" : 'asdasd',
    "IndssssiaPS" : 'asdasd',
    "DevaaaaaGroup" : "adasd"
}


def getVersionofConfig(myProperty):
    version = 0
    prodVersion = myProperty.getProductionVersion()
    stagingVersion = myProperty.getStagingVersion()
    latestVersion = myProperty.latestVersion

    version = prodVersion
    if version == 0:
        version = stagingVersion
        if version == 0:
            version = latestVersion

    return version


def fetchProperties():
    global config
    fp = open('configs.txt','r').readlines()
    fp = [x.strip() for x in fp]
    confstr = ','.join(fp)
    print(confstr)
    config['Configs']['property'] = confstr
    with open('config.ini', 'w') as configfile:    # save
        config.write(configfile)


def fetchCPCodes():
    global config,accountSwitchKey
    fetchProperties()
    configList = config['Configs']['property'].split(',')
    '''cpcodeList = config['Configs']['cpcode'].split(',')
    print(configList)
    print(cpcodeList)
    if len(cpcodeList) == 0:'''
    cpcodeList = []
    for prop in configList:
        print(prop)
        pyakamaiObj = pyakamai(accountSwitchKey)
        akamaiconfig = pyakamaiObj.client('property')
        akamaiconfig.config(prop)
        cplist = akamaiconfig.getCPCodes(akamaiconfig.getProductionVersion())
        for x in cplist:
            cpcodeList.append(x)
    print(cpcodeList)

    return cpcodeList


def createEventCenter():
    global accountSwitchKey,config
    #Prepare the payload for Event Creation
    payload = {
        "objects": [],
        "description": config['Subject']['description'],
        "name": config['Subject']['description'],
        "start":  config['Times']['startTime'],
        "end":  config['Times']['endTime'],
    }
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    print(payload)
    cpcodeList = []
    cpcodeList = fetchCPCodes()
    cpcodeList = list(set(cpcodeList))
    for cpCode in cpcodeList:
        newobj = {}
        newobj['type'] = 'CP_CODE'
        newobj['id'] = cpCode
        payload['objects'].append(newobj)

    eventobj_json = json.dumps(payload)

    
    ep = "/events/v3/events"
    params = {}
    params['accountSwitchKey'] = accountSwitchKey


    print(params)

    status,eventcreateJson = akhttp.postResult(ep,eventobj_json,headers=headers,params=params)
    print(status,eventcreateJson)
    if status == 200:
        print(json.dumps(eventcreateJson,indent=2))
        cpcodelist = ''
        for item1 in cpcodeList:
            if cpcodelist == '':
                cpcodelist = str(item1)
            else:
                cpcodelist = cpcodelist + ',' + str(item1)

        print(cpcodelist)
        print("Control Room Link:",'https://control.akamai.com/apps/event-center/#/schedule/events/{}/control-room'.format(str(eventcreateJson[0]['id'])))


        config['CP Codes Changed']['List'] = str(cpcodelist)
        config['EventCenter']['ControlRoomLink'] = 'https://control.akamai.com/apps/event-center/#/schedule/events/{}/control-room'.format(str(eventcreateJson[0]['id']))

        with open('config.ini', 'w') as configfile:    # save
            config.write(configfile)
        
        return True
    elif status == 409:
        print("Already event center exists !!")

    else:
        print(json.dumps(eventcreateJson,indent=2))
        print("Could not create the Event Center") 
        return False


def createProactiveTicket():
    f = open('config.ini','r')
    caseDescription = f.read()
    
    caseobj = {
        "severity": "3-Moderate",
        "subject": 'Proactive Ticket for changes-'+config['Subject']['description'],
        "description": caseDescription,
        "customer": "Verse",
        "endCustomerName": "",
        "partnerTicketNumber": "",
        "categoryType": "Technical",
        "doNotShowInPortalFlag": True,
        "userDetail": {
            "userName": "Achuthananda",
            "userPhone": "9986014033",
            "userEmail": "apadmana@akamai.com",
            "userCompany": "Akamai"
        },
        "subCategories": [
            {
                "displayName": "Product",
                "subCategoryType": "product",
                "subCategoryValue": "Adaptive Media Delivery"
            },
            {
                "displayName": "Problem",
                "subCategoryType": "problem",
                "subCategoryValue": "Failures/Errors"
            }
        ]
    }

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }


    caseobj_json = json.dumps(caseobj)

    ep = "/case-management/v2/cases"
    params = {}
    params['accountSwitchKey'] = accountSwitchKey

    status,createCaseJson = akhttp.postResult(ep,caseobj_json,headers=headers,params=params)
    if status == 200:
        print(status)
        print(createCaseJson)
        webexmessage = 'For Today\'s {} change , A proactive support ticket has been raised {} and the event center has been setup {}'.format(config['Subject']['description'],createCaseJson['caseId'],config['EventCenter']['ControlRoomLink'])
        print(webexmessage)
        return webexmessage
    else:
        return ''
       

def sendMessagetoSpace(webexspace,webexmessage):
    spaceArray = webexspace.split(',')
    bot = CiscoSparkAPI(access_token="O7c2c")
    for spaceName in spaceArray:
        spaceid = accessTokenDict[spaceName]
        bot.messages.create(spaceid, text=webexmessage)
        print("Sent the Webex message")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Support Ticket Raising Tool')
    parser.add_argument('--accountSwitchKey',required=True, default=None,help='Account SwitchKey')
    parser.add_argument('--sendWebex',required=True, default=None,help='Webex Notificaton Needed?')
    parser.add_argument('--space',required=False, default=None,help='Webex Space?')
    parser.add_argument('--ticket',required=False, default=True,help='Webex Space?')
    args = parser.parse_args()
    accountSwitchKey = args.accountSwitchKey

    status = createEventCenter()
    if status == True:
        if args.ticket != 'False':
            createTicketMessage = createProactiveTicket()
            if args.sendWebex != 'False':
                if createTicketMessage != '':
                    sendMessagetoSpace(args.space,createTicketMessage)
                else:
                    print("Error in Creating the Ticket")
            else:
                print(createTicketMessage)



