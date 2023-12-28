#!/usr/bin/env python3.6
import time,json
from pyakamai import pyakamai 


from ciscosparkapi import CiscoSparkAPI

accountSwitchKey = '1-5185s77UassaasN5:1-2RBL'
pyakamaiObj = pyakamai(accountSwitchKey)

diagnostic_tools  = pyakamaiObj.client('diagnostictools')

bot = CiscoSparkAPI(access_token="NDasdasdasdad")
spaceid = 'c6assa'


cpCodeList = open('cpcodelist.txt','r').readlines()
print(cpCodeList)

for i in range(1,2):
    for cpCode in cpCodeList:
        cpCode = cpCode.strip('\n')
        cpCode = cpCode.strip(' ')
        print(cpCode)
        try : 
            status_code,responsebody = diagnostic_tools.estatsPull(cpCode)
           
            seconds = time.time()

            resp_body = {}

            origin_resp_body = {}
            origin_resp_body['Time_Stamp'] = seconds
            origin_resp_body['2xx'] = 0.0
            origin_resp_body['3xx'] = 0.0
            origin_resp_body['4xx'] = 0.0
            origin_resp_body['5xx'] = 0.0

            edge_resp_body = {}
            edge_resp_body['Time_Stamp'] = seconds
            edge_resp_body['2xx'] = 0.0
            edge_resp_body['3xx'] = 0.0
            edge_resp_body['4xx'] = 0.0
            edge_resp_body['5xx'] = 0.0

            #print(json.dumps(body,indent=2))
            if status_code == 200:
                for i in responsebody['eStats']['originStatusCodeDistribution']:
                    if i['httpStatus'] in range(200,300):
                        origin_resp_body['2xx'] = round(origin_resp_body['2xx'] + i['percentage'],2)
                    elif i['httpStatus'] in range(300,400):
                        origin_resp_body['3xx'] = round(origin_resp_body['3xx'] + i['percentage'],2)
                    elif i['httpStatus'] in range(400,500):
                        origin_resp_body['4xx'] = round(origin_resp_body['4xx'] + i['percentage'],2)
                    elif i['httpStatus'] in range(500,600):
                        origin_resp_body['5xx'] = round(origin_resp_body['5xx'] + i['percentage'],2)


                for i in responsebody['eStats']['edgeStatusCodeDistribution']:
                    if i['httpStatus'] in range(200,300):
                        edge_resp_body['2xx'] = round(edge_resp_body['2xx'] + i['percentage'],2)
                    elif i['httpStatus'] in range(300,400):
                        edge_resp_body['3xx'] = round(edge_resp_body['3xx'] + i['percentage'],2)
                    elif i['httpStatus'] in range(400,500):
                        edge_resp_body['4xx'] = round(edge_resp_body['4xx'] + i['percentage'],2)
                    elif i['httpStatus'] in range(500,600):
                        edge_resp_body['5xx'] = round(edge_resp_body['5xx'] + i['percentage'],2)

                if i%500 == 0:
                    if  origin_resp_body['5xx'] > 3:
                        message = "Hello Team, estats monitoring shows that CP Code {} is seeing an increased origin 5x . Kindly Review".format(cpCode)
                        bot.messages.create(spaceid, text=message)
                    
                    if  edge_resp_body['5xx'] > 3:
                        message = "Hello Team, estats monitoring shows that CP Code {} is seeing an increased edge 5x. Kindly Review".format(cpCode)
                        bot.messages.create(spaceid, text=message)


                resp_body['CPCode'] = cpCode
                resp_body['edge'] = edge_resp_body
                resp_body['origin'] = origin_resp_body
        except:
            print("An exception occurred for CP Code {}".format(cpCode))

        print(resp_body)