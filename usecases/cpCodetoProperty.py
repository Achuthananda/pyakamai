import re,requests
import logging
import json,pandas
from pandas import ExcelWriter
import pandas as pd
from pyakamai import pyakamai

logging.basicConfig(filename='/Users/CustomerCode.txt',format='%(asctime)s %(message)s',level=logging.INFO)



edgercLocation = '/Users/apadmana/.edgerc'
accountSwitchKey = '19011-x'


cpCodeMap = {}
datajson = []
missedConfigs = []

groupMapping = {}
cofigGroupMap = {}


pyakamaiObj = pyakamai("1-585UN5:1-2RBL")


pyakamaiObj = pyakamai('AANA-427GY4:1-5G3LB')
akaconfig = pyakamaiObj.client('property')

arr = akaconfig.getallProperties()
for prop in arr:
    count = count + 1
    if count == 500:
        break
    config = prop
    print(count,':',config)
    
    akaconfig.config(config)


    version = akaconfig.getVersionofConfig()
   
    if version != 0:
        akaconfig = akaconfig(config)
        try:
            cpCodesList = akaconfig.getCPCodes(version)
            groupId = akaconfig.groupId
            cofigGroupMap[config] = groupMapping[groupId]
            for x in cpCodesList:
                if x not in cpCodeMap.keys():
                    cpCodeMap[x] = config
                else:
                    cpCodeMap[x] = cpCodeMap[x] + '\n' + config
        except Exception as e:
            logging.info('{}:Exception occured for {}'.format(e,config))
    else:
        missedConfigs.append(config)

try:
    for keys in cpCodeMap.keys():
        item = {}
        item['CPCode'] = keys
        item['Config'] = cpCodeMap[keys]
        item['Group'] = cofigGroupMap[cpCodeMap[keys].split('\n')[0]]
        datajson.append(item)
except Exception as e:
    logging.info('{}'.format(e))

print(datajson)
file_name = 'cpcodeMapping.xlsx'
writer = pandas.ExcelWriter(file_name, engine='xlsxwriter')
df = pandas.DataFrame(datajson)
df.to_excel(writer, sheet_name='CP',index = False)
writer.save()

print('Missed Cofnigs:',missedConfigs)