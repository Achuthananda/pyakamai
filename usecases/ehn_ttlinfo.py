from pyakamai import pyakamai 
import pandas
import argparse
import os
import traceback

edgercLocation = '~/.edgerc'
edgercLocation = os.path.expanduser(edgercLocation) # expand tilde. Python SDK doesn't handle tilde paths on Windows
ehn_list = []
accountSwitchKey = ''

directory = 'Outputs/EdgeHostnames'
if not os.path.exists(directory):
    os.makedirs(directory)  # Create the 'output' directory if it doesn't exist


def writeToExcel(arrayName,fileName,sheetName):
    writer = pandas.ExcelWriter(fileName, engine='xlsxwriter')
    df=pandas.json_normalize(arrayName)
    pandas.set_option('display.max_rows', df.shape[0]+1)
    df.to_excel(writer, sheet_name=sheetName,index = False)
    writer._save()


def getallEdgeHostNames():
    pyakamaiObj = pyakamai(accountSwitchKey)
    ehn_manager  = pyakamaiObj.client('ehn')
    
    result = ehn_manager.getallEdgeHostNames()
    for ehn in result['edgeHostnames']:
        item = {}
        item['EdgeHostName'] = ehn['recordName'] + '.' + ehn['dnsZone'] 
        item['TTL'] = ehn['ttl']
        item['TTLChange'] = 'No'
        if item['TTL'] != 21600:
            item['TTLChange'] = 'Yes'
        ehn_list.append(item)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='EHN Review')
    # Storage migration
    parser.add_argument('--accountSwitchKey',required=True, default=None,help='Account SwitchKey')
    args = parser.parse_args()
    print(args)

    if args.accountSwitchKey == None:
        print("Please Enter the Account SwitchKey in the format shown below")
        print("python3 ehn_ttlinfo.py -a B-C-1IasasE2OH8")
        exit(1)
    else:
        accountSwitchKey = args.accountSwitchKey
    try:

        allEHNList = getallEdgeHostNames()
        
        file_name = os.path.join(directory, args.accountSwitchKey + '_EHNTTLSettings.xlsx')
        sheetName = 'EHNTTLInfo'
        
        writeToExcel(ehn_list,file_name,sheetName)
        print("Done!")
    except Exception as e:
        print(e)
        track = traceback.format_exc()
        print(track)

'''
python3 ehn_ttlinfo.py --accountSwitchKey 1-15asssLAXIF:1-2RBL
'''