from akamaihttp import AkamaiHTTPHandler
import json

urllist = open('urls.txt','r').readlines()
urllist = [x.strip() for x in urllist]
print(urllist)

akhttp = AkamaiHTTPHandler('/Users/apadmana/.edgerc')

def listGTMDomains():
    listdomainsEP = '/config-gtm/v1/domains'
    params = {}
    params['accountSwitchKey'] = 'AasdasdL'
    result = akhttp.getResult(listdomainsEP,params)
    response = result[1]
    return [x['name'] for x in response['items']]

def listProperties(domain):
    listPropertyEP = '/config-gtm/v1/domains/{domain}/properties'.format(domain=domain)
    params = {}
    params['accountSwitchKey'] = 'asdasdL'
    result = akhttp.getResult(listPropertyEP,params)
    response = result[1]
    #print(json.dumps(response,indent=2))
    for items in response['items']:
        for lt in items['livenessTests']:
            livenesstestobject = ''
            if lt['hostHeader'] and lt['hostHeader'] :
                livenesstestobject = 'https://'+lt['hostHeader'] + lt['testObject']
            if livenesstestobject in urllist:
                print("Name:",items['name'])
                print("LivenessObject:",livenesstestobject)
                print("Status:Present")
            else:
                print("Name:",items['name'])
                print("LivenessObject:",livenesstestobject)
                print("Status:Absent")
        print('*'*80)

    #print(json.dumps(response,indent=2))





domainList = listGTMDomains()
for domain in domainList:
    listProperties(domain)




'''
ep = '/config-gtm/v1/domains/{domainName}/properties'
params = {}
result = akhttp.getResult(ep,params)
response = result[1]
#print(response['geoLocation']['countryCode'],response['geoLocation']['continent'])
return response['geoLocation']['countryCode'],response['geoLocation']['continent']'''