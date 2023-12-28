import argparse
from pyakamai import pyakamai
import json

def writeToExcel(arrayName,fileName,sheetName):
    import pandas
    writer = pandas.ExcelWriter(fileName, engine='xlsxwriter')
    df=pandas.json_normalize(arrayName)
    pandas.set_option('display.max_rows', df.shape[0]+1)
    df.to_excel(writer, sheet_name=sheetName,index = False)
    writer._save()

cacheArray = []
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Review Caching of API Definition')
    parser.add_argument('--accountSwitchKey',required=True, default=None,help='Account SwitchKey')
    parser.add_argument('--apiEndpoint',required=True, default=None,help='apiEndPoint')
    parser.add_argument('--version',required=True, default=None,help='Version')
    
    args = parser.parse_args()
    accountSwitchKey = args.accountSwitchKey
    apiEndpoint = args.apiEndpoint
    version = args.version

    pyakamaiObj = pyakamai(accountSwitchKey)
    akamaiconfig = pyakamaiObj.client('apidefinition')
    cacheSettings = akamaiconfig.listCacheSettings(apiEndpoint,version)
    for resource_id, cacheresource in cacheSettings['resources'].items():
        print(cacheresource)
        item = {}
        item['path'] = cacheresource['path']
        item['Methods'] = cacheresource['methods']
        item['option'] = cacheresource['option']
        if cacheresource['maxAge'] == None:
            item['maxage'] = 'NA'
        else:
            item['maxage'] = str(cacheresource['maxAge']['duration']) + cacheresource['maxAge']['unit']
        item['serveStale'] = cacheresource['serveStale']
        if cacheresource['preRefreshing'] == None or cacheresource['preRefreshing']['enabled'] == False:
            item['preRefreshing'] = 'Not Enabled'
        else:
            item['preRefreshing'] = cacheresource['preRefreshing']['enabled'] + cacheresource['preRefreshing']['value']
        item['inheritsFromEndpoint'] = cacheresource['inheritsFromEndpoint']
        print(item)
        cacheArray.append(item)

    filename = "{}.xlsx".format(apiEndpoint)
    writeToExcel(cacheArray,filename,'cacheereview')

'''
python3 cachesettingexport.py --accountSwitchKey F-asd5:1-2RBL --apiEndpoint 579246 --version 55
'''