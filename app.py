from pyakamai import pyakamai
import json


'''
pyakamaiObj = pyakamai()


akamaiconfig = pyakamaiObj.client('apidefinition')
cacheSettings = akamaiconfig.listCacheSettings(579246,55)
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
    if cacheresource['preRefreshing'] == None:
        item['preRefreshing'] = 'Not Enabled'
    else:
        item['preRefreshing'] = cacheresource['preRefreshing']['enabled'] + cacheresource['preRefreshing']['value']
    item['inheritsFromEndpoint'] = cacheresource['inheritsFromEndpoint']
    print(item)
print("Hello World")
'''


'''
pyakamaiObj = pyakamai("1-5sss85ssUN5:1-2RBL")

from pyakamai import pyakamai
pyakamaiObj = pyakamai('1-6JsHG**X')
akamaiconfig = pyakamaiObj.client('property')
akamaiconfig.config('TimesClone1')
version = akamaiconfig.getProductionVersion()
arr = akamaiconfig.getHostNames(version)
for x in arr:
    print(x)

    


if version >= 0:
    product = akamaiconfig.getProduct()
    print(product)'''


'''
#------------------------Datastream Start-------------------------------------------
from pyakamai import pyakamai
import json
pyakamaiObj = pyakamai('1-58sRBL')


from pyakamai import pyakamai
import json
pyakamaiObj = pyakamai('1-5L')
dsClient = pyakamaiObj.client('datastream')


f = open('datastream.json','r')
data = json.load(f)
streampayload = json.dumps(data)
print(streampayload)


streamcreation = dsClient.createStream(streampayload,activate=True)
print(streamcreation)


datasets = dsClient.getDatasets()
print(json.dumps(datasets,indent=2))


groupJson = dsClient.listGroups()
print(json.dumps(groupJson,indent=2))

streamJson = dsClient.listStreams(65552)
print(json.dumps(streamJson,indent=2))


from pyakamai import pyakamai
import json
pyakamaiObj = pyakamai('1-1NC95D')
dsClient = pyakamaiObj.client('datastream')





#------------------------EDNS Start-------------------------------------------
from pyakamai import pyakamai
pyakamaiObj = pyakamai('F-AC-1:1-2RBL')

ednsClient = pyakamaiObj.client('edns')
for ednszone in ednsClient.listZones()['zones']:
    print(ednszone['zone'])


#------------------------AkamaiProperty Start-------------------------------------------
from pyakamai import pyakamai
pyakamaiObj = pyakamai('1-5BL') 
akamaiconfig = pyakamaiObj.client('property')
akamaiconfig.config('hf-apix.hotstar.com')

configName = akamaiconfig.search('hf-apix.hotstar.com')

hostNames = akamaiconfig.getHostNames(akamaiconfig.getProductionVersion())


akamaiconfig.getCPCodes(akamaiconfig.getProductionVersion())




akamaiconfig.printPropertyInfo()


#------------------------MSL Start-------------------------------------------
from pyakamai import pyakamai
pyakamaiObj = pyakamai('1-5BL') 
mslConfig = pyakamaiObj.client('msl')
mslConfig.stream('2002471')
mslConfig.printStreamInfo()'''


'''#------------------------CPS Start-------------------------------------------
from pyakamai import pyakamai
pyakamaiObj = pyakamai('B-3X') 
cpsClient = pyakamaiObj.client('cps')


enrollments = cpsClient.listEnrollments()

print(json.dumps(enrollments,indent=2))'''

'''
#------------------------LDS Start-------------------------------------------
from pyakamai import pyakamai
pyakamaiObj = pyakamai('B-3') 
ldsClient = pyakamaiObj.client('lds')
#ldsList = ldsClient.listLogConfigurations('gtm-properties')
ldsList = ldsClient.listLogConfigurations('cpcode-products')
print(json.dumps(ldsList,indent=2))
'''

'''#------------------------Purge Start-------------------------------------------
from pyakamai import pyakamai
pyakamaiObj = pyakamai(section='ccu') #Akamai Technologies Assets
purgeClient = pyakamaiObj.client('purge')


print(purgeClient.deletebyCPCode([912248],'staging'))
print(purgeClient.deletebyCPCode([912248],'production'))
print(purgeClient.invalidatebyCPCode([912248],'production'))
print(purgeClient.deletebyURL(['http://www.achuth-purgetest.edgesuite.net/images/5.jpg','http://www.achuth-purgetest.edgesuite.net/images/9.jpg'],'staging'))
print(purgeClient.invalidatebyURL(['http://www.achuth-purgetest.edgesuite.net/images/5.jpg','http://www.achuth-purgetest.edgesuite.net/images/9.jpg'],'staging'))
print(purgeClient.deletebyCacheTag(['acmpjs','acmpimages'],'staging'))
print(purgeClient.invalidatebyCacheTag(['acmpjs','acmpimages'],'production'))'''


'''
#------------------------EHN Start-------------------------------------------
pyakamaiObj = pyakamai('F-AC-82:1-2RBL')
ehnClient = pyakamaiObj.client('ehn')
ehnList = ehnClient.getallEdgeHostNames()

productList = ehnClient.listProducts()
print(json.dumps(productList,indent=2))
'''

'''
#------------------------AkamaiCasemanagement Start-------------------------------------------
from pyakamai import pyakamai
import json
pyakamaiObj = pyakamai()
caseManagementClient = pyakamaiObj.client('case')
caseList = caseManagementClient.listAllActiveCases(accountIds='1-585UN5')
print(json.dumps(caseList,indent=2))

'''




'''
Case Management
Network Lists
Event Center
Netstorage
ATC
ChinaCDN
Image Manager
Identity and Access Management
Edgeworkers
EdgeKV
Appsec
Reporting
API Definition
App & API Protector
Bot Manager
Client Access Control
Cloudlets
CP Codes
Diagnostic Tools
Global Traffic Management
SiteShield
'''

'''
def updateAllRecord(accountSwitchKey,zone,ttl):
    headers = {'Accept-Type': 'application/json'}

    params = {}
    params["accountSwitchKey"] = accountSwitchKey

    getZonesReecordsEP = '/config-dns/v2/zones/{zone}/recordsets'.format(zone=zone)
    resultjson = prdHttpCaller.getResult(getZonesReecordsEP,headers=headers,params=params)
    if resultjson[0] == 200:
        print(json.dumps(resultjson[1],indent=2))
        recordArray = resultjson[1]['recordsets']
        for records in recordArray:
            records['ttl'] = int(ttl)
            updateRecord(zone,records['name'],records['type'],records)
    else:
        print("Failed to get the records for the zone")
        print(json.dumps(resultjson,indent=2))
    print('*'*80)

'''
'''
from pyakamai import pyakamai
import json
pyakamaiObj = pyakamai('1-51185U99999N5')
caseManagementClient = pyakamaiObj.client('case')
caseList = caseManagementClient.listAllCases()
for case in caseList:
    if case['status'] not in ['Closed','Mitigated / Solution Provided']:
        if case['severity'] != '3-Low Impact':
            print(case)

'''
#print(json.dumps(caseList,indent=2))
