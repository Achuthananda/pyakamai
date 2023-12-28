import unquote
from pyakamai import pyakamai
try:
    def getCountryContinent(ip_address):
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


ip_addresslist = ['184.51.199.100', '2.22.225.95', '184.51.199.108', '2.16.170.209', '184.51.199.119', '2.22.225.36', '92.122.52.158', '2.16.106.6', '23.216.10.19', '2.18.240.103', '2.18.240.99', '2.16.106.28', '2.16.170.201', '2.16.106.15', '2.17.40.62', '23.216.10.20', '2.21.33.36', '2.16.106.36', '2.18.240.93', '2.16.170.198', '2.22.225.80', '2.21.33.55', '104.97.78.60', '23.216.10.5', '184.51.199.110', '95.100.156.173', '23.216.10.9', '2.17.210.87', '2.16.170.208', '104.97.78.53', '23.216.10.22', '2.18.240.97', '95.101.2.196', '2.18.240.55', '2.16.106.7', '2.17.40.97', '2.18.240.76', '2.21.33.38', '95.101.137.12', '72.246.216.155', '23.216.10.16', '95.101.2.170', '2.21.33.46', '95.100.156.159', '72.246.150.55', '2.17.210.124', '95.101.2.178', '104.71.131.8', '2.17.210.108', '2.22.225.4', '2.22.225.63', '2.17.40.31', '92.122.52.61', '2.17.210.94', '72.246.150.76', '23.203.249.100', '92.122.52.7', '2.22.225.52', '95.101.137.69', '2.17.40.135', '2.17.40.48', '23.203.249.47', '95.101.137.38', '23.216.10.39', '95.101.2.197', '2.21.33.70', '2.16.170.223', '23.203.249.46', '92.122.52.133', '92.122.52.71', '95.101.137.23', '2.21.33.69', '95.101.2.200', '2.17.40.88', '92.122.52.143', '2.22.225.15', '2.17.210.60', '2.22.225.88', '104.71.131.5', '2.16.170.214', '2.21.33.68', '2.16.170.233', '72.246.216.139', '23.203.249.111', '104.97.78.59', '72.246.216.142', '2.21.33.45', '2.22.225.38', '23.216.10.13', '2.21.33.54', '72.246.216.150', '23.216.10.8', '23.216.10.31', '92.122.52.54', '2.16.170.184', '104.71.131.23']

accountSwitchKey = '89798'
datajson = []
pyakamaiObj = pyakamai(accountSwitchKey)
ssconfig = pyakamaiObj.client('ss')
status,result = ssconfig.listSSMaps()
if status == 200:
    for ssmap in result['siteShieldMaps']:
        if ssmap['ruleName'] == 's-122.akaiedge.net':
            for ip in ip_addresslist:
                belongs = False
                for cidr in  ssmap['currentCidrs']:
                    if isIPofCIDR(ip,cidr):
                        belongs = True
                        country,continent = getCountryContinent(ip)
                        if continent != 'EU':
                                print(unquote(ip))
                                #print("Part of CIDR {} and continent {}".format(cidr,continent))
                if belongs == False:
                    print("Not Part of any CIDR")
        print('*'*80)
