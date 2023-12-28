#python gtmreport.py -a 'AANA-4P168S:1-2RBL' -f 'test.xlsx'

from akamaihttp import AkamaiHTTPHandler
import json,pandas,re,os
import optparse

edgercLocation = '~/.edgerc'
edgercLocation = os.path.expanduser(edgercLocation) # expand tilde. Python SDK doesn't handle tilde paths on Windows


akhttp = AkamaiHTTPHandler(edgercLocation)

gtmreportArray = []

parser = optparse.OptionParser()
parser.add_option(
        '-f', '--file',
        action='store', type='string', dest='fileName',
        help='FileName.')

parser.add_option(
        '-a', '--accountSwitchKey',
        action='store', type='string', dest='accountSwitchKey',
        help='AccountSwitchKey.')

(options, args) = parser.parse_args()
print(options)

if options.accountSwitchKey:
    accountSwitchKey =  options.accountSwitchKey

fileName = 'GTMReport.xlsx'
if options.fileName:
    fileName =  options.fileName

def writeToExcel(arrayName,fileName,sheetName):
    writer = pandas.ExcelWriter(fileName, engine='xlsxwriter')
    df=pandas.json_normalize(arrayName)
    pandas.set_option('display.max_rows', df.shape[0]+1)
    df.to_excel(writer, sheet_name=sheetName,index = False)
    writer.save()

def listGTMDomains():
    listdomainsEP = '/config-gtm/v1/domains'
    params = {}
    params['accountSwitchKey'] = accountSwitchKey
    result = akhttp.getResult(listdomainsEP,params)
    response = result[1]
    return [x['name'] for x in response['items']]

def listProperties(domain):
    listPropertyEP = '/config-gtm/v1/domains/{domain}/properties'.format(domain=domain)
    params = {}
    params['accountSwitchKey'] = accountSwitchKey
    result = akhttp.getResult(listPropertyEP,params)
    response = result[1]
    #print(json.dumps(response,indent=2))
    for items in response['items']:
        print(items['name'])
        item = {}
        item['GTM Property'] = items['name'] + '.' + domain
        item['backup CNAME']  = ''
        item['backupIP'] = ''
        item['origins'] = []
        item['Liveness Test URL'] = ''
        if items['backupCName']:
            item['backup CNAME'] = items['backupCName']
        if items['backupIp']:
            item['backupIP'] = items['backupIp']
        
        for origins in items['trafficTargets']:
            print(origins['servers'])
            for x in origins['servers']:
                item['origins'].append(x)
        
        item['Liveness Test URL'] = ''
        for lt in items['livenessTests']:
            if lt['hostHeader'] and lt['hostHeader'] :
                item['Liveness Test URL'] = lt['testObject']

        print(item)
        gtmreportArray.append(item)


domainList = listGTMDomains()
for domain in domainList:
    listProperties(domain)

writeToExcel(gtmreportArray,fileName,'GTMDetails')

