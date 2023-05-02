from ..common.commonutilities import print_log,getProductId
import json
import sys

def createCPCode(contractId,groupId,hostName,akhttp,accountSwitchKey=None):
    try:
        params = {}
        if accountSwitchKey != None:
            params["accountSwitchKey"] = accountSwitchKey
        params["contractId"] = contractId
        params["groupId"] = groupId


        create_cpcode = {
            "productId": getProductId(),
            "cpcodeName": hostName
        }

        cpcode_data = json.dumps(create_cpcode)

        createCPCodeEndPoint = '/papi/v1/cpcodes'
        headers = {'Content-Type': 'application/json'}#,
                   #'PAPI-Use-Prefixes': True}

        #print_log(cpcode_data)
        #print_log(headers)

        status,createCPCodeJson = akhttp.postResult(createCPCodeEndPoint,cpcode_data,headers,params)
        if status == 201:
            print_log(createCPCodeJson)
            cpCode = createCPCodeJson['cpcodeLink'].split('?')[0].split('/')[4].split('_')[1]
            print_log('Successfully created the CP Code {} for {}'.format(cpCode,hostName))
            return cpCode
        else:
            print_log('Failed to create the CP Code for {} and status code is {}.'.format(hostName,status))
            return 0
    except Exception as e:
        print('{}:Error Creating the CP Code for {}'.format(e,hostName),file=sys.stderr)
        print_log('{}:Error Creating the CP Code for {}'.format(e,hostName))
        exit(3)
