
from urllib.parse import unquote
import logging
from akamaihttp import AkamaiHTTPHandler
import json
import pandas
from pandas import ExcelWriter
import xlsxwriter
import random
import ipaddress
from pyakamai import pyakamai

logging.basicConfig(filename='/Users/logs.txt',format='%(asctime)s %(message)s',level=logging.INFO)

try:
    def getCountry(ip_address):
        from ip2geotools.databases.noncommercial import DbIpCity
        import pycountry_convert as pc
        response = DbIpCity.get(ip_address, api_key='free')
        continent = pc.country_alpha2_to_continent_code(response.country)
        return response.country,continent

    def isIPofCIDR(ip,cidrblock):
        from ipaddress import ip_network, ip_address
        net = ip_network(cidrblock)
        return ip_address(ip) in net

except Exception as e:
    print("Error getting the field Value")

accountSwitchKey = '89798'
datajson = []
pyakamaiObj = pyakamai(accountSwitchKey)
ssconfig = pyakamaiObj.client('ss')
status,result = ssconfig.listSSMaps()
if status == 200:
    for ssmap in result['siteShieldMaps']:
        if ssmap['ruleName'] == 's-122.akaiedge.net':
            row = {}
            row['Map Name | Siteshield ID'] = ssmap['mapAlias'] + '|' + str(ssmap['id'])
            row['Siteshield Map'] = ssmap['ruleName']
            row['Ack status'] = 'Done' if ssmap['acknowledged'] else 'Pending'
            row['Map Rule'] = ssmap['mcmMapRuleId']
            row['SS Continent'] = ''
            row['SS Country'] = ''

            print(ssmap['ruleName'])
            continentlist = []
            countryList = []
            for cidr in ssmap['currentCidrs']:
                num_to_select = 2                   
                ip_list = [str(ip) for ip in ipaddress.IPv4Network(cidr)]
                list_of_random_ips = random.sample(ip_list, num_to_select)
                for ipAddress in list_of_random_ips:
                    #print('Fetching the continent for {}'.format(ipAddress))
                    country,continent = getCountry(ipAddress)
                    if country == 'IT':
                        print(country,continent,cidr,ipAddress)
                    if continent not in continentlist:
                        continentlist.append(continent)
                    if country not in countryList:
                        countryList.append(country)
            
            for x in continentlist:
                row['SS Continent'] = row['SS Continent'] + ',' + x
            
            for x in countryList:
                row['SS Country'] = row['SS Country'] + ',' + x

            print('*'*80)
            datajson.append(row)

'''
file_name = 'ssmap_country.xlsx'
writer = pandas.ExcelWriter(file_name, engine='xlsxwriter')
df = pandas.DataFrame(datajson)
df.to_excel(writer, sheet_name='SS',index = False)
writer.save()
'''