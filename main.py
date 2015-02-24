import reqParse
import pdb

if __name__ == "__main__":
	#pdb.set_trace()
	res = reqParse.parseReq("input")
	for i in res.items():
		print i