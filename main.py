import reqParse
import require
import pdb
import os
import lan

if __name__ == "__main__":
    branch_name = ''
    while branch_name not in ['master', '6.1', '6.0.1']:
        branch_name = raw_input("At the what branch we should check requirements? ")
        if branch_name == 'master':
            branch = 'master'
        elif branch_name == '6.1':
            branch = 'openstack-ci/fuel-6.1/2014.2'
        elif branch_name == '6.0.1':
            branch = 'openstack-ci/fuel-6.0.1/2014.2'
    #pdb.set_trace()
    gerritAccount = lan.loginToLaunchpad()
    with open("2ndReq", 'r') as f:
        rq2 = require.Require(reqParse.parseReq(f))
    with open('req', 'r') as req_file:
        for repo in req_file:
            print "Repos:", repo
<<<<<<< HEAD
            req_url = 'https://review.fuel-infra.org/gitweb?p=openstack/' + repo.strip() + '.git;a=blob_plain;f=requirements.txt;hb=refs/heads/' + branch
=======
            req_url = 'https://review.fuel-infra.org/gitweb?p=openstack/' + repo.strip() + '.git;a=blob_plain;f=requirements.txt;hb=refs/heads/master'
>>>>>>> 8641242da880d12d0fbe534bf5d6930f74da5866
            r = lan.getRequirementsFromUrl(req_url, gerritAccount)
            rq1 = require.Require(reqParse.parseReq(r))
            rq = require.Require.merge(rq1.packs, rq2.packs)
            for key in rq1.packs.keys():
                print "{0} {1}".format(key, rq[key])
    #os.system("./emailSend.sh {0} "'"{1}"'"".format("asteroid566@gmail.com", rq.items()))
    #for i in rq1.packs.items():
    #	print i
    #for key in rq1.packs.keys():
    #	print "{0} {1}".format(key, rq[key])