from pyakamai import pyakamai
import json

'''from pyakamai import pyakamai
pyakamaiObj = pyakamai()
akamaiconfig = pyakamaiObj.client('property')

akamaiconfig.config('achuth-purgetest.com')
version = akamaiconfig.getProductionVersion()
print(version)

if version >= 0:
    product = akamaiconfig.getProduct()
    print(product)'''


'''
#------------------------Datastream Start-------------------------------------------
pyakamaiObj = pyakamai('F-AC-1526355:1-2RBL')


dsClient = pyakamaiObj.client('datastream')


groupJson = dsClient.listGroups()
print(json.dumps(groupJson,indent=2))

streamJson = dsClient.listStreams(225177)
print(json.dumps(streamJson,indent=2))


#------------------------EDNS Start-------------------------------------------
from pyakamai import pyakamai
pyakamaiObj = pyakamai('F-AC-1526355:1-2RBL')

ednsClient = pyakamaiObj.client('edns')
for ednszone in ednsClient.listZones()['zones']:
    print(ednszone['zone'])


#------------------------AkamaiProperty Start-------------------------------------------
from pyakamai import pyakamai
pyakamaiObj = pyakamai() 
akamaiconfig = pyakamaiObj.client('property')
configName = akamaiconfig.search('www.achuth-purgetest.edgesuite.net')


akamaiconfig.config('hf-apix.hotstar.com')
akamaiconfig.getCPCodes(akamaiconfig.getProductionVersion())




akamaiconfig.printPropertyInfo()


#------------------------MSL Start-------------------------------------------
from pyakamai import pyakamai
pyakamaiObj = pyakamai('1-585UN5:1-2RBL') 
mslConfig = pyakamaiObj.client('msl')
mslConfig.stream('2002471')
mslConfig.printStreamInfo()'''


'''#------------------------CPS Start-------------------------------------------
from pyakamai import pyakamai
pyakamaiObj = pyakamai('B-3-16OEUPX') 
cpsClient = pyakamaiObj.client('cps')


enrollments = cpsClient.listEnrollments()

print(json.dumps(enrollments,indent=2))'''

'''
#------------------------LDS Start-------------------------------------------
from pyakamai import pyakamai
pyakamaiObj = pyakamai('B-3-16OEUPX') 
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
pyakamaiObj = pyakamai('F-AC-2341982:1-2RBL')
ehnClient = pyakamaiObj.client('ehn')
ehnList = ehnClient.getallEdgeHostNames()

productList = ehnClient.listProducts()
print(json.dumps(productList,indent=2))
'''

'''
#------------------------AkamaiCasemanagement Start-------------------------------------------
from pyakamai import pyakamai
import json
pyakamaiObj = pyakamai('F-AC-1526355:1-2RBL')
caseManagementClient = pyakamaiObj.client('case')
caseList = caseManagementClient.listAllActiveCases(accountIds='F-AC-1526355:1-2RBL')
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

