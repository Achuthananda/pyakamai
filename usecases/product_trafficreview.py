import pandas
import requests
import os
import json
import numpy as np
from openpyxl import load_workbook
import json
from akamaiproperty import AkamaiPropertyManager
import logging
from akamaihttp import AkamaiHTTPHandler
from pyakamai import pyakamai
import traceback


edgercLocation = '~/.edgerc'
edgercLocation = os.path.expanduser(edgercLocation)

configProductArray = []
doneconfigs = []
akhttp = AkamaiHTTPHandler(edgercLocation)

directory = 'Outputs/ProductReview'
if not os.path.exists(directory):
    os.makedirs(directory)  # Create the 'output' directory if it doesn't exist


def getAllProperties(accountSwitchKey):
    fileName = os.path.join(directory, accountSwitchKey + '_configs.txt')

    if not os.path.isfile(fileName):
        print("Getting all the list of configs from all contracts and groups..")
        pm = AkamaiPropertyManager(edgercLocation,accountSwitchKey)
        propertiesList = pm.getallProperties()
        np.savetxt(fileName, np.array(propertiesList), fmt="%s")


def get_url_extension(url):
    return os.path.splitext(url)[1][1:]

def readConfigList(accountSwitchKey):
    global doneconfigs
    print("Reading the config list..")
    fileName = os.path.join(directory, accountSwitchKey + '_configs.txt')
    fp = open(fileName,'r')
    arr = fp.readlines()
    arr = [x.strip() for x in arr]
    doneconfigFileName = 'output/'+accountSwitchKey + '_doneconfigs.txt'
    if not os.path.isfile(doneconfigFileName):
        return list(set(arr))
    else:
        fp1 = open(doneconfigFileName,'r')
        arr1 = fp1.readlines()
        doneconfigs = arr1
        if len(arr1) != 0:
            print("There are already some configs whose settings are fetched !")
            arr1 = [x.strip() for x in arr1]
            return list(set(arr) - set(arr1))
        else:
            print("Fetching config settings for the first time!")
            return list(set(arr))


def readCompletedSettings(accountSwitchKey):
    global configProductArray
    fileName = os.path.join(directory, accountSwitchKey + '_results.json')
    if os.path.isfile(fileName):
        fp = open(fileName, 'r')
        configProductArray = json.load(fp)
        print(configProductArray)
    
def writeToExcel(arrayName,fileName,sheetName):
    writer = pandas.ExcelWriter(fileName, engine='xlsxwriter')
    df=pandas.json_normalize(arrayName)
    pandas.set_option('display.max_rows', df.shape[0]+1)
    df.to_excel(writer, sheet_name=sheetName,index = False)
    writer._save()

def getTopUrls(cpcodeList,accountSwitchKey,interval = 1):
    from datetime import datetime,timedelta
    urlArray = []
    try:
        for i in range(0, len(cpcodeList), 100):
            data = {}
            data['objectIds'] = cpcodeList[i:i+100]
           
            data["objectType"]=  "cpcode"
            data['metrics'] = ["allEdgeHits", "allOriginHits", "allHitsOffload"]

            jsondata = json.dumps(data)

            end = datetime.today().replace(hour=0,minute=0,second=0,microsecond=0).isoformat()
            start = (datetime.today()-timedelta(days=31)).replace(hour=0,minute=0,second=0,microsecond=0).isoformat()

            params =    {
                            'accountSwitchKey': accountSwitchKey,
                            'start':start,
                            'end':end
                        }

            headers = {
                "accept": "application/json",
                "content-type": "application/json"
            }

            ep = "reporting-api/v1/reports/urlhits-by-url/versions/1/report-data"
        
            result = akhttp.postResult(ep,jsondata,headers=headers,params=params)
            code = result[0]
            body = result[1]
            for urldata in body['data']:
                urlArray.append(urldata['hostname.url'])

    except Exception as e:
        print("Exception in fetching the Top URLs-{}".format(e))
    
    return urlArray


def fetchProductDetailsSettings(configList,accountSwitchKey):
    global configProductArray
    global doneconfigs

    try:
        for config in configList:
            print("Fetching the Config Settings from {}".format(config))
            print(accountSwitchKey)
            pyakamaiObj = pyakamai(accountSwitchKey) #Novi
            akaconfig = pyakamaiObj.client('property')
            akaconfig.config(config)
            if akaconfig._invalidconfig == True:
                print("Invalid Config Continuing.")
                print('*'*80)
                continue

            item = {}
            item['Contract'] = akaconfig.contractId
            item['GroupId'] = akaconfig.groupId
            item['PropertyName'] = config
            product = akaconfig.getProduct()
            version = akaconfig.getVersionofConfig()
            hostnames = akaconfig.getHostNames(version)
            cpcodeList = akaconfig.getCPCodes(version)
            urlArray = getTopUrls(cpcodeList,accountSwitchKey,interval = 1)
            urlExtensionArray = []
            for url in urlArray:
                ext = get_url_extension(url)
                if ext != '':
                    urlExtensionArray.append(ext)

            urlExtensionArray = list(set(urlExtensionArray))

            item['Hostnames'] = '' 
            for hostname in hostnames:
                if item['Hostnames'] == '':
                    item['Hostnames'] = hostname
                else:
                    item['Hostnames'] = item['Hostnames'] + '\n' + hostname

            item['Product'] = product
            item['File Extensions'] = ','.join(urlExtensionArray)
            print(item)

            configProductArray.append(item)
            json_object = json.dumps(configProductArray, indent=2)
                
            # Writing to sample.json
            fileName = os.path.join(directory, args.accountSwitchKey + '_results.json')
            with open(fileName, "w") as outfile:
                outfile.write(json_object)

            doneconfigs.append(config)
            doneconfigFileName = os.path.join(directory, args.accountSwitchKey + '_doneconfigs.txt')
            doneconfigs = [x.strip() for x in doneconfigs]
            np.savetxt(doneconfigFileName, np.array(doneconfigs), fmt="%s")
            print('*'*80)
    except Exception as e:
        logging.info('Exception occured for {}-{}'.format(config,e))
        print(e)
        print("Oops!", e.__class__, "occurred.")
        doneconfigFileName = os.path.join(directory, args.accountSwitchKey + '_doneconfigs.txt')
        doneconfigs = [x.strip() for x in doneconfigs]
        np.savetxt(doneconfigFileName, np.array(doneconfigs), fmt="%s")
        json_object = json.dumps(configProductArray, indent=2)
        fileName = os.path.join(directory, args.accountSwitchKey + '_results.json')
        with open(fileName, "w") as outfile:
            outfile.write(json_object)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Traffic Review Tool')
    # Storage migration
    parser.add_argument('--accountSwitchKey',required=True, default=None,help='Account SwitchKey')
    args = parser.parse_args()
    print(args)

    try:
        getAllProperties(args.accountSwitchKey)
        configArray = readConfigList(args.accountSwitchKey)
        readCompletedSettings(args.accountSwitchKey)

        fetchProductDetailsSettings(configArray,args.accountSwitchKey)

        sheetName = 'ProductInfo'
        fileName = os.path.join(directory, args.accountSwitchKey + '_productSettings.xlsx')

        writeToExcel(configProductArray,fileName,sheetName)

    except Exception as e:
        track = traceback.format_exc()
        print(track)
    

'''
python3 product_trafficreview.py --accountSwitchKey AAasdasX
python3 product_trafficreview.py --accountSwitchKey F-Aasdasd
'''






   
