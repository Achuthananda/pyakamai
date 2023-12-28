from akamaiproperty import AkamaiProperty,AkamaiPropertyManager
import pandas
import logging
import optparse
import os
from openpyxl import load_workbook
import numpy as np

logging.basicConfig(filename='ss_scan.txt',format='%(asctime)s %(message)s',level=logging.INFO)

edgercLocation = '~/.edgerc'
edgercLocation = os.path.expanduser(edgercLocation) # expand tilde. Python SDK doesn't handle tilde paths on Windows
accountSwitchKey = ''

ssorignArray = []
parser = optparse.OptionParser()
parser.add_option(
        '-a', '--accountSwitchKey',
        action='store', type='string', dest='accountSwitchKey',
        help='AccountSwitchKey.')

parser.add_option(
        '-s', '--start',
        action='store', type='int', dest='start',
        help='StartIndex.')

parser.add_option(
        '-e', '--end',
        action='store', type='int', dest='end',
        help='EndIndex.')

def writeToExcel(arrayName,fileName,sheetName):
    writer = pandas.ExcelWriter(fileName, engine='xlsxwriter')
    df=pandas.json_normalize(arrayName)
    pandas.set_option('display.max_rows', df.shape[0]+1)
    df.to_excel(writer, sheet_name=sheetName,index = False)
    writer.save()

def readConfigList():
    fp = open('config.txt','r')
    arr = fp.readlines()
    arr = [x.strip() for x in arr]
    return arr

def getAllProperties():
    pm = AkamaiPropertyManager(edgercLocation,accountSwitchKey)
    propertiesList = pm.getallProperties()
    np.savetxt("config.txt", np.array(propertiesList), fmt="%s")


def getSSInfo(configArray,startIndex,endIndex):
    for i in range(startIndex,endIndex+1):
        print("Fetching the SS Details of the Config:",configArray[i])
        akaconfig = AkamaiProperty(edgercLocation,configArray[i],accountSwitchKey)
        item = {}
        item['PropertyName'] = configArray[i]
        item['Production Active'] = 'FALSE'
        version = 0 
        version = akaconfig.getProductionVersion()
        if version == 0:
            version = akaconfig.getStagingVersion()
            if version == 0:
                version = akaconfig.latestVersion
        else:
            item['Production Active'] = 'TRUE'
        try:
            ruleTree = akaconfig.getRuleTree(version)
            ss_map = akaconfig.getSiteShieldMap(version)
            sr_map = akaconfig.getSureRouteCustomMaps(version)
            #print(sr_map)
            origins = akaconfig.getOrigins(version)
            hostnames = akaconfig.getHostNames(version)

            item['Hostnames'] = '' 
            for hostname in hostnames:
                if item['Hostnames'] == '':
                    item['Hostnames'] = hostname
                else:
                    item['Hostnames'] = item['Hostnames'] + '\n' + hostname

            item['Origins'] = '' 
            for origin in origins:
                if '{{builtin.AK_HOST}}' in origin:
                    oldorigin = origin
                    for x in hostnames:
                        origin = oldorigin
                        origin = origin.replace("{{builtin.AK_HOST}}", x)
                        if item['Origins'] == '':
                            item['Origins'] = origin
                        else:
                            item['Origins'] = item['Origins'] + '\n' + origin
                else:
                    if item['Origins'] == '':
                            item['Origins'] = origin
                    else:
                        item['Origins'] = item['Origins'] + '\n' + origin

            item['SR Map'] = ''
            for sr in sr_map:
                if item['SR Map'] == '':
                    item['SR Map'] = sr
                else:
                    item['SR Map'] = item['SR Map'] + '\n' + sr

            item['SS Map'] = '' 
            for ss in ss_map:
                if item['SS Map'] == '':
                    item['SS Map'] = ss
                else:
                    item['SS Map'] = item['SS Map'] + '\n' + ss

            ssorignArray.append(item)
        except Exception as e:
            logging.info('Exception occured for {}-{}'.format(configArray[i],e))


if __name__ == "__main__":
    (options, args) = parser.parse_args()
    print(options)
    if options.accountSwitchKey == None:
        print("Please Enter the Account SwitchKey in the format shown below")
        print("python3 ss_origin_scan.py -a BH8")
        exit(1)
    else:
        accountSwitchKey = options.accountSwitchKey

    getAllProperties()
    configArray = readConfigList()
    
    if options.start == None or options.end == None:
        start = 0
        end = len(configArray) - 1
    else:
        start = options.start
        end = options.end

    getSSInfo(configArray,start,end)
   
    sheetName = '{}_{}'.format(start,end)
    file_name = 'SS_Scan.xlsx'
    if not os.path.isfile(file_name):
        writer = pandas.ExcelWriter(file_name, engine='xlsxwriter')
        df = pandas.DataFrame(ssorignArray)
        df.to_excel(writer, sheet_name=sheetName,index = False)
    else:
        book = load_workbook(file_name)
        writer = pandas.ExcelWriter(file_name, engine='openpyxl') 
        writer.book = book
        df = pandas.DataFrame(ssorignArray)
        df.to_excel(writer, sheet_name=sheetName,index = False)

    writer.save()
    print("Done!")