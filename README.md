# pyakamai - The Akamai SDK for Python
[![Package Version](http://img.shields.io/pypi/v/boto3.svg?style=flat)](https://pypi.org/project/pyakamai/)
[![Python Versions](https://img.shields.io/pypi/pyversions/boto3.svg?style=flat)](https://pypi.org/project/pyakamai/)

pyakamai is the Akamai CDN Software Development Kit (SDK) for Python, which allows Python developers to write software that makes use of services like Akamai Delivery ,Security Configs and many more. 

pyakamai (pronounced pie-akamai) is maintained and published by Achuthananda and a group of enthusiastic Akamai developers.

The advantage of pyakamai is application developers need not know about the underlying API calls and their usage. Application developers can just focus on getting their work done programmatically using the objects of pyakamai.


### Getting Starterd
In order to use this configuration, you need to:
* Set up your credential files as described in the [doc](https://techdocs.akamai.com/developer/docs/set-up-authentication-credentials).
* When working through this process you need to give grants for the various APIs as needed. You can have any number of sections in your .edgerc file.


### Install pip package available
```
$ pip install pyakamai
```

or install from source with:

```
$ git clone https://github.com/Achuthananda/pyakamai
$ cd pyakamai
$ python -m pip install -r requirements.txt
$ python -m pip install -e .
```


# Using pyakamai

## Using AkamaiProperty

### Print Hostnames
```
>>> from pyakamai import pyakamai
>>> akamaiconfig = pyakamaiObj.client('property')
>>> akamaiconfig.config('test_bulkseach_update_1')
>>> hostnamesList = akamaiconfig.getHostNames(akamaiconfig.getProductionVersion())
>>> for hostname in hostnamesList:
>>>     print(hostname)
```

### Print Basic Information
```
>>> akamaiconfig.printPropertyInfo()
Property Name: test_bulkseach_update_1
Contract Id: ctr_C-1IE2OHM
Group Id: grp_163363
Active Staging Version: 18
Active Production Version: 18
```

### Create a new version
```
>>> akamaiconfig.createVersion(18)
'78'
```

### Get rule Tree
```
>>>akamaiconfig.getRuleTree(18)
{'accountId': 'act_B-C-1IE2OH8', 'contractId': 'ctr_C-1IE2OHM', 'groupId': 'grp_163363', 'propertyId': 'prp_605086', 'propertyName': 'test_bulkseach_update_1', 'propertyVersion': 18, 'etag': 'd0d28a6b71e665144955f7f7e1ff214933d119d7', 'rules':.....}
```

### Activate the config
```
>>>akamaiconfig.activateStaging(18,"testing activation",["apadmana@akamai.com"])
True
```

## Using AkamaiEDNS
```
from pyakamai import pyakamai
pyakamaiObj = pyakamai('ACCOUNT-SWITCH-KEY')

ednsClient = pyakamaiObj.client('edns')
for ednszone in ednsClient.listZones()['zones']:
    print(ednszone['zone'])

```

## Using Akamai MSL
```
>>>from pyakamai import pyakamai
>>>pyakamaiObj = pyakamai(''ACCOUNT-SWITCH-KEY)
>>>mslConfig = pyakamaiObj.client('msl')

>>>mslConfig.stream('2002471')
>>>mslConfig.printStreamInfo()

Stream Name: ssselecthd2dash2323
Stream Id: 2002471
Allowed IPs: ['203.2.47.34', '125.212.85.190', '213.200.155.163', '15.110.20.2', '14.13.11.61/32', '14.43.83.134']
Format: DASH
Origin: {'id': 16532, 'hostName': '012-dn001-sssesslectasdashd2dash.akamaiorigin.net', 'cpcode': 759459}
Provisioning Status: PROVISIONED
```


## Using Akamai Purge
```
>>> from pyakamai import pyakamai
>>> pyakamaiObj = pyakamai(section='ccu') #Akamai Technologies Assets
>>> purgeClient = pyakamaiObj.client('purge')
>>> 
>>> 
>>> print(purgeClient.deletebyCPCode([912248],'staging'))
{'httpStatus': 201, 'detail': 'Request accepted', 'supportId': 'edcs-NP5QvoTVwkpnjdADva1U9c', 'purgeId': 'edcs-NP5QvoTVwkpnjdADva1U9c', 'estimatedSeconds': 5}
>>> print(purgeClient.deletebyCPCode([912248],'production'))
{'httpStatus': 201, 'detail': 'Request accepted', 'supportId': 'edcp-NTTmPZzCdHbYAMaVdTKyd3', 'purgeId': 'edcp-NTTmPZzCdHbYAMaVdTKyd3', 'estimatedSeconds': 5}
>>> print(purgeClient.invalidatebyCPCode([912248],'production'))
{'httpStatus': 201, 'detail': 'Request accepted', 'supportId': 'eicp-NVQycBX9FkCPHvEfv8Ntx1', 'purgeId': 'eicp-NVQycBX9FkCPHvEfv8Ntx1', 'estimatedSeconds': 5}
>>> print(purgeClient.deletebyURL(['http://www.achuth-purgetest.edgesuite.net/images/5.jpg','http://www.achuth-purgetest.edgesuite.net/images/9.jpg'],'staging'))
{'httpStatus': 201, 'detail': 'Request accepted', 'supportId': 'edus-Na3M2qwxAMioicEEWj1Scz', 'purgeId': 'edus-Na3M2qwxAMioicEEWj1Scz', 'estimatedSeconds': 5}
>>> print(purgeClient.invalidatebyURL(['http://www.achuth-purgetest.edgesuite.net/images/5.jpg','http://www.achuth-purgetest.edgesuite.net/images/9.jpg'],'staging'))
{'httpStatus': 201, 'detail': 'Request accepted', 'supportId': 'eius-NfB5EvSnXdz7B36rhjxRxU', 'purgeId': 'eius-NfB5EvSnXdz7B36rhjxRxU', 'estimatedSeconds': 5}
>>> print(purgeClient.deletebyCacheTag(['acmpjs','acmpimages'],'staging'))
{'httpStatus': 201, 'detail': 'Request accepted', 'supportId': 'edts-NhiHSoKVaXULwJj9eS48EU', 'purgeId': 'edts-NhiHSoKVaXULwJj9eS48EU', 'estimatedSeconds': 5}
>>> print(purgeClient.invalidatebyCacheTag(['acmpjs','acmpimages'],'production'))
{'httpStatus': 201, 'detail': 'Request accepted', 'supportId': 'eitp-PYjibvc6uyRKcM31gn5GxY', 'purgeId': 'eitp-PYjibvc6uyRKcM31gn5GxY', 'estimatedSeconds': 5}
```

## Using Akamai CPS
```
>>> from pyakamai import pyakamai
>>> pyakamaiObj = pyakamai('B-3-16OEUPX') 
>>> cpsClient = pyakamaiObj.client('cps')
>>> 
>>> 
>>> enrollments = cpsClient.listEnrollments()

print(json.dumps(enrollments,indent=2))
>>> 
>>> print(json.dumps(enrollments,indent=2))
{
  "enrollments": [
    {
      "location": "/cps/v2/enrollments/65586",
      "ra": "lets-encrypt",
      "validationType": "dv",
      "certificateType": "san",
      "certificateChainType": "default",
      "networkConfiguration": {
        "geography": "core",
        "secureNetwork": "enhanced-tls",
        "mustHaveCiphers": "ak-akamai-2020q1",
        "preferredCiphers": "ak-akamai-2020q1",
        "disallowedTlsVersions": [
          "TLSv1",
          "TLSv1_1"]}}]}
```

## Using Akamai LDS

```
>>> from pyakamai import pyakamai
>>> pyakamaiObj = pyakamai('B-3-16OEUPX') 
>>> ldsClient = pyakamaiObj.client('lds')
>>> ldsList = ldsClient.listConfigs('cpcode-products')

>>> print(json.dumps(ldsList,indent=2))
[
  {
    "id": 707034,
    "status": "expired",
    "startDate": "2021-06-13",
    "endDate": "2021-07-13",
    "logSource": {
      "links": [
        {
          "rel": "self",
          "href": "/lds-api/v3/log-sources/cpcode-products/1-788273"
        },
        {
          "rel": "cpcode-products",
          "href": "/lds-api/v3/log-sources/cpcode-products"
        },
        {
          "rel": "log-sources",
          "href": "/lds-api/v3/log-sources"
        }
      ],
      "type": "cpcode-products",
      "id": "1-788273",
      "cpCode": "788273 - demo.grinwis.com-pristine",
      "products": [
        "Ion Standard"
      ],
      "logRetentionDays": 8
    },
    "aggregationDetails": {
      "type": "byLogArrival",
      "deliveryFrequency": {
        "id": "1",
        "value": "Every 24 hours",
        "links": [
          {
            "rel": "self",
            "href": "/lds-api/v3/log-configuration-parameters/delivery-frequencies/1"
          },
          {
            "rel": "deliveryFrequencies",
            "href": "/lds-api/v3/log-configuration-parameters/delivery-frequencies"
          }
        ]
      }
    },
    "contactDetails": {
      "mailAddresses": [
        "jgrinwis@akamai.com"
      ],
      "contact": {
        "id": "F-CO-3289943",
        "value": "John Grinwis - phone: +31615514552",
        "links": [
          {
            "rel": "self",
            "href": "/lds-api/v3/log-configuration-parameters/contacts/F-CO-3289943"
          },
          {
            "rel": "contacts",
            "href": "/lds-api/v3/log-configuration-parameters/contacts"
          }
        ]
      }
    },
    "deliveryDetails": {
      "type": "httpsns4",
      "domainPrefix": "jgrinwis",
      "cpcodeId": 789214,
      "directory": "/logs"
    },
    "encodingDetails": {
      "encoding": {
        "id": "3",
        "value": "GZIP",
        "links": [
          {
            "rel": "self",
            "href": "/lds-api/v3/log-configuration-parameters/encodings/3"
          },
          {
            "rel": "encodings",
            "href": "/lds-api/v3/log-configuration-parameters/encodings"
          }
        ]
      }
    },
    "logFormatDetails": {
      "logIdentifier": "test_grinwis",
      "logFormat": {
        "id": "2",
        "value": "combined",
        "links": [
          {
            "rel": "self",
            "href": "/lds-api/v3/log-configuration-parameters/log-formats/2"
          },
          {
            "rel": "logFormats",
            "href": "/lds-api/v3/log-configuration-parameters/log-formats"
          }
        ]
      }
    },
    "messageSize": {
      "id": "1",
      "value": "50 MB (approx. 300 MB uncompressed logs)",
      "links": [
        {
          "rel": "self",
          "href": "/lds-api/v3/log-configuration-parameters/message-sizes/1"
        },
        {
          "rel": "messageSizes",
          "href": "/lds-api/v3/log-configuration-parameters/message-sizes"
        }
      ]
    },
    "links": [
      {
        "rel": "self",
        "href": "/lds-api/v3/log-configurations/707034"
      },
      {
        "rel": "get-log-configurations-for-log-source",
        "href": "/lds-api/v3/log-sources/cpcode-products/1-788273/log-configurations",
        "title": "Get Log Configurations for the same log source"
      },
      {
        "rel": "get-log-configurations-for-log-source-type",
        "href": "/lds-api/v3/log-sources/cpcode-products/log-configurations",
        "title": "Get Log Configurations for the same log source type"
      },
      {
        "rel": "update-log-configuration",
        "href": "/lds-api/v3/log-configurations/707034",
        "method": "PUT",
        "title": "Update Log Configuration"
      },
      {
        "rel": "delete-log-configuration",
        "href": "/lds-api/v3/log-configurations/707034",
        "method": "DELETE",
        "title": "Delete Log Configuration"
      }
    ]
  },

```