from pyakamai import pyakamai
import json
import pandas as pd


accountSwitchKey = 'F-AC-2234437'
filename = 'input.xlsx'


if __name__ == "__main__":
    df = pd.read_excel(filename)
    for index, row in df.iterrows():
        config = row['Config']
        config = config.strip()
        if config not in  ['bizimages.withfloats.com']:
            hostname = row['Hostname']
            print("Updating the config {}".format(config))
            #print("Config:",config)
            pyakamaiObj = pyakamai(accountSwitchKey=accountSwitchKey,edgercLocation='~/.edgerc', section='default',debug=False, verbose=False)
            akamaiconfig = pyakamaiObj.client('property')

            akamaiconfig.config(config)

            version = akamaiconfig.createVersion(akamaiconfig.getVersionofConfig())
            hostnameArray = akamaiconfig.getHostNames(version)
            
            status = akamaiconfig.addHostname(version,hostname,'all.nowfloats.com.edgekey.net')
            if status == True:
                print("Added the hostanme {} successfully for the config {}".format(hostname,config))
            else:
                print("Failed to add the hostanme {} for the config {}".format(hostname,config))
            for hostname in hostnameArray:
                status= akamaiconfig.removeHostname(version,hostname)
                if status == True:
                    print("Removed the hostanme {} successfully for the config {}".format(hostname,config))
                else:
                    print("Removal of the hostanme {} Failed for the config {}".format(hostname,config))

            fp = open('rule.json','r')
            data = {}
            data = json.load(fp)

            ruleTree = akamaiconfig.getRuleTree(version)
            ruleTree['rules'] = data

            propruleInfo_json = json.dumps(ruleTree, indent=2)
            print("Updating the rules for the config {}".format(config))
            addRuleStatus = akamaiconfig.updateRuleTree(version, propruleInfo_json)
            if addRuleStatus == True:
                print("Updated the Rule successfully for the config {}".format(config))
                updateNoteStatus = akamaiconfig.addVersionNotes(version, 'Decommision')
                if updateNoteStatus == True:
                    print("Updated the Notes successfully for the config {}".format(config))
                    stagingactivationStatus = akamaiconfig.activateStaging(version, 'Decommision', ["apadmana@akamai.com"])
                    if stagingactivationStatus == True:
                        print("Activated the Config to Staging for the config {}".format(config))
                    else:
                        print("Failed to Activate the Notes for the config {}".format(config))
                else:
                    print("Failed to Update the Notes for the config {}".format(config))
            else:
                print("Failed the update the rule successfully for the config {}".format(config))

            print('*'*80)
