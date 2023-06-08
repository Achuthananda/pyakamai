from akamaihttp import AkamaiHTTPHandler
import os
import argparse
import json
import requests
from akamai.edgegrid import EdgeGridAuth, EdgeRc
from urllib.parse import urljoin
import sys
import random
import string
import uuid
from commonutilities import print_log

import configparser

settingsconfig = configparser.ConfigParser()
settingsconfig.read('config.ini')
edgercLocation = settingsconfig['Edgerc']['location']
edgercLocation = os.path.expanduser(edgercLocation)
akhttp = AkamaiHTTPHandler(edgercLocation,settingsconfig['Edgerc']['section'])

def createConfig(accountSwitchKey,configName,contractId,groupId,hostNameArray):
    try:
        createConfigEP = '/appsec/v1/configs'
        params = {}
        if accountSwitchKey != None:
            params['accountSwitchKey'] = accountSwitchKey
        
        
        headers = {
            "accept": "application/json",
            "content-type": "application/json"
        }
        payload = {
            "name": configName,
            "description": "Test",
            "contractId": contractId,
            "groupId": groupId,
            "hostnames": hostNameArray
        }
        datajson = json.dumps(payload,indent=2)

        status,createAppSecConfigJson = akhttp.postResult(createConfigEP,datajson,headers,params)
        if status == 201:
            #print(createEnrollmentJson)
            configId = createAppSecConfigJson['configId']
            print('Successfully created the App Sec Config and Config Id is {}'.format(configId))
            return configId
        else:
            print_log(status)
            print_log("Failed to create the App Sec Config")
            return 0
    except Exception as e:
        print('{}:Error create the App Sec Config'.format(e),file=sys.stderr)
        return 0

    return configId

def createSecurityPolicy(accountSwitchKey,configId,version,securityPolicyName):
    try:
        createSPEP = '/appsec/v1/configs/{}/versions/{}/security-policies'.format(configId,version)
        params = {}
        if accountSwitchKey != None:
            params['accountSwitchKey'] = accountSwitchKey
        
        
        headers = {
            "accept": "application/json",
            "content-type": "application/json"
        }

        letters = string.ascii_letters
        policyPrefix = "".join(random.sample(letters,3))

        payload = {
            "policyName": securityPolicyName,
            "policyPrefix": policyPrefix
        }

        datajson = json.dumps(payload,indent=2)

        status,createAppSecPolicyJson = akhttp.postResult(createSPEP,datajson,headers,params)
        if status == 200:
            #print(createEnrollmentJson)
            policyId = createAppSecPolicyJson['policyId']
            print_log('Successfully created the App Sec Policy {} and  Id is {}'.format(securityPolicyName,policyId))
            return policyId
        else:
            print_log(status)
            print_log("Failed to create the App Sec Policy")
            return 0
    except Exception as e:
        print('{}:Error create the App Sec Policy'.format(e),file=sys.stderr)
        return 0

    return configId


def createAppSecConfig(accountSwitchKey,configName,contractId,groupId,securityPolicyName,hostNameArray):
    try:
        configId = createConfig(accountSwitchKey,configName,contractId,groupId,hostNameArray)
        if configId != 0 :
            policyId = createSecurityPolicy(accountSwitchKey,configId,1,securityPolicyName)
            if policyId != 0:
                print_log("Config {} and Security Policy {} has been created".format(configName,securityPolicyName))
            else:
                print_log("Config {} and Security Policy {} creation Failed".format(configName,securityPolicyName))
        else:
            print_log("Security Config {} Creation Failed".format(configName))

        return configId,policyId

    except Exception as e:
        print('{}:Error Creating the Enrollment'.format(e),file=sys.stderr)
        exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Times CDN Onboarding Tool.')
    # Storage migration
    parser.add_argument('--accountSwitchKey', default=None,help='Account SwitchKey')
    parser.add_argument('--name', required=True,help='Name of the AppSec Config')
    parser.add_argument('--contractId', required=True,help='ContractID')
    parser.add_argument('--groupId', required=True,help='groupId')
    parser.add_argument('--securityPolicyName', required=True,help='securityPolicyName')
    parser.add_argument('--hostnames', required=True,help='Comma Separated Hostnames')
    parser.add_argument('--logfile', help='Log File Name')
    

    args = parser.parse_args()
    jobId = str(uuid.uuid1())
    logfilepath = ''

    curdir = os.getcwd()
    dirpath = os.path.dirname(curdir + '/logs')
    logfilepath = dirpath + "/"  + jobId+'.txt'

    if args.logfile:
        logfilepath = dirpath + "/logs/" + args.logfile

    sys.stdout = open(logfilepath, 'w+')

    hostNameArray = args.hostnames.split(',')
    configId,policyId = createAppSecConfig(args.accountSwitchKey,args.name,args.contractId,args.groupId,args.securityPolicyName,hostNameArray)
    if configId != 0:
        print('Succesfully Created the App Sec Config and the config Id is {} and Policy Id is {}'.format(configId,policyId),file=sys.stderr)
    else:
        print('Failed to Created the App Sec Config',file=sys.stderr)
   
'''
python ksdCreate.py --logfile ksdlog --accountSwitchKey 1-6JHGX --name TimesAppSecConfigNew --groupId 223702 --contractId 1-1NC95D --securityPolicyName Policy1 --hostnames 'example1.edgesuite.net'
Akamai Professional Services
'''


