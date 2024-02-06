import pandas
import os
from openpyxl import load_workbook
import numpy as np
import json
from pyakamai import pyakamai
import traceback



edgercLocation = '~/.edgerc'
edgercLocation = os.path.expanduser(edgercLocation)

hostname_list = []
originSettingsArray = []
doneconfigs = []

def readConfigList(accountSwitchKey):
    global doneconfigs
    print("Reading the config list..")
    fileName = accountSwitchKey +  '_configs.txt'
    fp = open(fileName,'r')
    arr = fp.readlines()
    arr = [x.strip() for x in arr]
    doneconfigFileName = accountSwitchKey + '_doneconfigs.txt'
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

def getAllProperties(accountSwitchKey):
    fileName = accountSwitchKey +  '_configs.txt'
    if not os.path.isfile(fileName):
        print("Getting all the list of configs from all contracts and groups..")
        pyakamaiObj = pyakamai(accountSwitchKey)
        pmmanager = pyakamaiObj.client('propertymanager')
        propertiesList = pmmanager.getallProperties()
        print(propertiesList)
        np.savetxt(fileName, np.array(propertiesList), fmt="%s")

def readCompletedOriginSettings(accountSwitchKey):
    global originSettingsArray
    fileName = accountSwitchKey + '_results.json'
    if os.path.isfile(fileName):
        fp = open(fileName, 'r')
        originSettingsArray = json.load(fp)
        print(originSettingsArray)
    

def writeToExcel(arrayName,fileName,sheetName):
    writer = pandas.ExcelWriter(fileName, engine='xlsxwriter')
    df=pandas.json_normalize(arrayName)
    pandas.set_option('display.max_rows', df.shape[0]+1)
    df.to_excel(writer, sheet_name=sheetName,index = False)
    writer._save()



def fetchOriginSettings(configList,accountSwitchKey):
    global originSettingsArray
    global doneconfigs
    for config in configList:
        try:
            pyakamaiObj = pyakamai(accountSwitchKey)
            myconfig = pyakamaiObj.client('property')
            print("Config:",config)
            myconfig.config(config)
            version = myconfig.getVersionofConfig()
            behaviorList = myconfig._getBehaviorParsedList(version)

            for pmbehaviors in behaviorList:
                if pmbehaviors['behavior']['name'] == 'origin':
                    #print(json.dumps(pmbehaviors,indent=2))
                    item = {}
                    item['Config'] = config
                    item['Hostnames'] = myconfig.getHostNames(version)
                    print(item['Hostnames'])
                    if pmbehaviors['behavior']['options']['originType'] == 'CUSTOMER':
                        if 'hostname' in  pmbehaviors['behavior']['options']:
                            item['OriginHostname'] = pmbehaviors['behavior']['options']['hostname']
                        else:
                            item['OriginHostname'] = 'Empty'
                        item['OriginType'] =pmbehaviors['behavior']['options']['originType']
                        if 'forwardHostHeader' in pmbehaviors['behavior']['options']:
                            item['ForwardHostHeader'] = pmbehaviors['behavior']['options']['forwardHostHeader']
                        else:
                            item['ForwardHostHeader'] = 'Empty'

                        if 'cacheKeyHostname' in pmbehaviors['behavior']['options']:
                            item['CacheKeyHostName'] = pmbehaviors['behavior']['options']['cacheKeyHostname']
                        else:
                            item['CacheKeyHostName'] = 'Empty'

                        item['Verifications Settings'] = ""
                        if 'verificationMode' in pmbehaviors['behavior']['options']:
                            if pmbehaviors['behavior']['options']['verificationMode'] == "PLATFORM_SETTINGS":
                                item['Verifications Settings'] = "Use Platform Settings"
                            if pmbehaviors['behavior']['options']['verificationMode'] == "THIRD_PARTY":
                                item['Verifications Settings'] = "Third Party Settings"
                            if pmbehaviors['behavior']['options']['verificationMode'] == "CUSTOM":
                                item['Verifications Settings'] = "Choose Your Own"

                        item['Match Common Name'] = 'NA'
                        item['Trust'] = 'NA'
                        item['Akamai Cert Store'] = 'NA'
                        item['Third Party Certificate Store'] = 'NA'
                        item['Custom Authorities Set'] = []
                        item['Pinned Certificates Set'] = []

                        if 'verificationMode' in pmbehaviors['behavior']['options']:
                            if pmbehaviors['behavior']['options']['verificationMode'] == "CUSTOM":
                                item['Match Common Name'] = pmbehaviors['behavior']['options']['customValidCnValues']
                                if pmbehaviors['behavior']['options']['originCertsToHonor'] == 'STANDARD_CERTIFICATE_AUTHORITIES':
                                    item['Trust'] = 'Akamai-managed Certificate Authorities Sets'
                                    if 'akamai-permissive' in pmbehaviors['behavior']['options']['standardCertificateAuthorities']:
                                        item['Akamai Cert Store'] = 'Enabled'
                                    else:
                                        item['Akamai Cert Store'] = 'Disabled'

                                    if 'THIRD_PARTY_AMAZON' in pmbehaviors['behavior']['options']['standardCertificateAuthorities']:
                                        item['Third Party Certificate Store'] = 'Enabled'
                                    else:
                                        item['Third Party Certificate Store'] = 'Disabled'
                                    
                                if pmbehaviors['behavior']['options']['originCertsToHonor'] == 'CUSTOM_CERTIFICATES':
                                    item['Trust'] = 'Specific Certificate Pinning'
                                    for pinnedCerts in pmbehaviors['behavior']['options']['customCertificates']:
                                        item['Pinned Certificates Set'].append(pinnedCerts['sha1Fingerprint'])

                                
                                if pmbehaviors['behavior']['options']['originCertsToHonor'] == 'CUSTOM_CERTIFICATE_AUTHORITIES':
                                    item['Trust'] = 'Custom Certificate Authority Set'
                                    for cacerts in pmbehaviors['behavior']['options']['customCertificateAuthorities']:
                                        item['Custom Authorities Set'].append(cacerts['sha1Fingerprint'])

                                
                                if pmbehaviors['behavior']['options']['originCertsToHonor'] == 'COMBO':
                                    item['Trust'] = 'Any of the the three Settings'
                                    if 'akamai-permissive' in pmbehaviors['behavior']['options']['standardCertificateAuthorities']:
                                        item['Akamai Cert Store'] = 'Enabled'
                                    else:
                                        item['Akamai Cert Store'] = 'Disabled'

                                    if 'THIRD_PARTY_AMAZON' in pmbehaviors['behavior']['options']['standardCertificateAuthorities']:
                                        item['Third Party Certificate Store'] = 'Enabled'
                                    else:
                                        item['Third Party Certificate Store'] = 'Disabled'

                                    #Custom Cert Settings
                                    for cacerts in pmbehaviors['behavior']['options']['customCertificateAuthorities']:
                                        item['Custom Authorities Set'].append(cacerts['sha1Fingerprint'])

                                    #Pinned Cert Settings
                                    item['Pinned Certificates Set'] = []
                                    for pinnedCerts in pmbehaviors['behavior']['options']['customCertificates']:
                                        item['Pinned Certificates Set'].append(pinnedCerts['sha1Fingerprint'])

                    elif pmbehaviors['behavior']['options']['originType'] == 'NET_STORAGE':
                        if pmbehaviors['behavior']['options']['netStorage'] != None:
                            item['OriginHostname'] = pmbehaviors['behavior']['options']['netStorage']['downloadDomainName']
                            item['OriginType'] = pmbehaviors['behavior']['options']['originType']
                            item['ForwardHostHeader'] = 'NA'
                            item['Verifications Settings'] = "Use Platform Settings"
                            item['Match Common Name'] = 'NA'
                            item['Trust'] = 'NA'
                            item['Akamai Cert Store'] = 'NA'
                            item['Third Party Certificate Store'] = 'NA'
                            item['Custom Authorities Set'] = []
                            item['Pinned Certificates Set'] = []
                    
                    elif pmbehaviors['behavior']['options']['originType'] == 'MEDIA_SERVICE_LIVE':
                        if pmbehaviors['behavior']['options']['mslorigin'] != None:
                            item['OriginHostname'] = pmbehaviors['behavior']['options']['mslorigin']
                            item['OriginType'] = pmbehaviors['behavior']['options']['originType']
                            item['ForwardHostHeader'] = 'NA'
                            item['Verifications Settings'] = "NA"
                            item['Match Common Name'] = 'NA'
                            item['Trust'] = 'NA'
                            item['Akamai Cert Store'] = 'NA'
                            item['Third Party Certificate Store'] = 'NA'
                            item['Custom Authorities Set'] = []
                            item['Pinned Certificates Set'] = []
                    else:
                        print("Undefined...")

                    print(item)
                    originSettingsArray.append(item)
                    json_object = json.dumps(originSettingsArray, indent=2)
                    
                    # Writing to sample.json
                    fileName = accountSwitchKey + '_results.json'
                    with open(fileName, "w") as outfile:
                        outfile.write(json_object)

            doneconfigs.append(config)
            doneconfigFileName = accountSwitchKey + '_doneconfigs.txt'
            doneconfigs = [x.strip() for x in doneconfigs]
            np.savetxt(doneconfigFileName, np.array(doneconfigs), fmt="%s")
            print('*'*80)
            
        except Exception as e:
            doneconfigFileName = accountSwitchKey + '_doneconfigs.txt'
            doneconfigs = [x.strip() for x in doneconfigs]
            np.savetxt(doneconfigFileName, np.array(doneconfigs), fmt="%s")
            json_object = json.dumps(originSettingsArray, indent=2)
            fileName = accountSwitchKey + '_results.json'
            with open(fileName, "w") as outfile:
                outfile.write(json_object)
            track = traceback.format_exc()
            print(track)

        
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Origin Settings Tool')
    # Storage migration
    parser.add_argument('--accountSwitchKey',required=True, default=None,help='Account SwitchKey')
    args = parser.parse_args()
    print(args)

    try:
        getAllProperties(args.accountSwitchKey)
        configArray = readConfigList(args.accountSwitchKey)
        readCompletedOriginSettings(args.accountSwitchKey)

        fetchOriginSettings(configArray,args.accountSwitchKey)

        sheetName = 'OriginInfo'
        fileName = args.accountSwitchKey+'_originsettings.xlsx'
        writeToExcel(originSettingsArray,fileName,sheetName)

    except Exception as e:
        track = traceback.format_exc()
        print(track)
    

'''
python3 fetchoriginsettings.py --accountSwitchKey F-AC-4960455

'''






   
