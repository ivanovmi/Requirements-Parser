import reqParse
import require
import pdb

if __name__ == "__main__":
	#pdb.set_trace()
	rq1 = require.Require(reqParse.parseReq("ceilometerReq"))
	rq2 = require.Require(reqParse.parseReq("saharaReq"))
	#print r.packs
	rq = require.Require.merge(rq1.packs, rq2.packs)
	for i in rq.items():
		print i
	#for i in rq1.packs.items():
	#	print i