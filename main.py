import reqParse
import require
import pdb
import os
import lan

if __name__ == "__main__":
	#pdb.set_trace()
	req_url = 'https://review.fuel-infra.org/gitweb?p=openstack/horizon.git;a=blob_plain;f=requirements.txt;hb=refs/heads/master'
	gerritAccount = lan.loginToLaunchpad()

	r = lan.getRequirementsFromUrl(req_url, gerritAccount)
	rq1 = require.Require(reqParse.parseReq(r))
	with open("2ndReq", 'r') as f:
		rq2 = require.Require(reqParse.parseReq(f))
	rq = require.Require.merge(rq1.packs, rq2.packs)
	for i in rq.items():
		print i
	#os.system("./emailSend.sh {0} "'"{1}"'"".format("asteroid566@gmail.com", rq.items()))
	#for i in rq1.packs.items():
	#	print i
	#for key in rq1.packs.keys():
	#	print "{0} {1}".format(key, rq[key])