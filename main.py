import reqParse
import require
import pdb
import os

if __name__ == "__main__":
	#pdb.set_trace()
	rq1 = require.Require(reqParse.parseReq("ceilometerReq"))
	rq2 = require.Require(reqParse.parseReq("saharaReq"))
	rq = require.Require.merge(rq1.packs, rq2.packs)
	for i in rq.items():
		print i
	os.system("./emailSend.sh {0} "'"{1}"'"".format("asteroid566@gmail.com", rq.items()))
	#for i in rq1.packs.items():
	#	print i