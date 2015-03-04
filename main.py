import reqParse
import require
import pdb
import os
import lan

if __name__ == "__main__":
    #pdb.set_trace()
    gerritAccount = lan.loginToLaunchpad()
    with open("2ndReq", 'r') as f:
        rq2 = require.Require(reqParse.parseReq(f))
    with open('req', 'r') as req_file:
        for repo in req_file:
            print "Repos:", repo
<<<<<<< HEAD
            req_url = 'https://review.fuel-infra.org/gitweb?p=openstack/' + repo.strip() + '.git;a=blob_plain;f=requirements.txt;hb=refs/heads/master'
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
=======
            req_url = 'https://review.fuel-infra.org/gitweb?p=openstack/horizon.git;a=blob_plain;f=requirements.txt;hb=refs/heads/master'
            r = lan.getRequirementsFromUrl(req_url, gerritAccount)
            rq1 = require.Require(reqParse.parseReq(r))
            rq = require.Require.merge(rq1.packs, rq2.packs)
            #for i in rq.items():
            #    print i
    #os.system("./emailSend.sh {0} "'"{1}"'"".format("asteroid566@gmail.com", rq.items()))
    #for i in rq1.packs.items():
    #	print i
            for key in rq1.packs.keys():
                print "{0} {1}".format(key, rq[key])
>>>>>>> 79f0eacf59eff31a3264ce37d0e00374117f84a2
