import reqParse
import require
import pdb
import os
import lan
import json
#import reporter.report as report

if __name__ == "__main__":
    branch_name = ''
    while branch_name not in ['master', '6.1', '6.0.1']:
        branch_name = 'master'
        #branch_name = raw_input("At the what branch we should check requirements? ")
        if branch_name == 'master':
            branch = 'master'
        elif branch_name == '6.1':
            branch = 'openstack-ci/fuel-6.1/2014.2'
        elif branch_name == '6.0.1':
            branch = 'openstack-ci/fuel-6.0.1/2014.2'
    #pdb.set_trace()
    gerritAccount = lan.loginToLaunchpad()
    json_file = open('requirements.json', 'w')
    json_file.write('{\n\t"projects": [\n\t')
    with open("2ndReq", 'r') as f:
        rq2 = require.Require(reqParse.parseReq(f))
    with open('req', 'r') as req_file:
        for repo in req_file:
            print '\n'*3, "Repos:", repo
            req_url = 'https://review.fuel-infra.org/gitweb?p=openstack/' + repo.strip() + '.git;a=blob_plain;f=requirements.txt;hb=refs/heads/' + branch
            r = lan.getRequirementsFromUrl(req_url, gerritAccount)
            rq1 = require.Require(reqParse.parseReq(r))
            rq = require.Require.merge(rq1.packs, rq2.packs)
            json_file.write('\t{\n'+'\t'*2+json.dumps(repo.strip())+': {\n')
            for key in rq1.packs.keys():
                print len(key)
                json_file.write('\t'*3+json.dumps(key)+':'+json.dumps(rq[key])+',\n')
                print "{0}:{1}".format(key, rq[key])
            json_file.write('\t'*2+'}},\n')
    json_file.write('\t'+']\n}')
            #os.system("./emailSend.sh {0} "'"{1}"'"".format("asteroid566@gmail.com", rq.items()))
            #for i in rq1.packs.items():
            #	print i
            #for key in rq1.packs.keys():
            #	print "{0} {1}".format(key, rq[key])
'''
    def generate_output():
        # read example JSON
        with open("../sample.json") as json_file:
            json_data = json.load(json_file)
        report.generate_report.generate_rst(json_data)

generate_output()'''