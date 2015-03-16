import require_utils
import pdb

#pdb.set_trace()
#print require_utils.Require.correlate({"python-lock":"", "pyok":"", "pypbr":""}, "python-pbr")
with open('control', 'r') as f:
	res = require_utils.Require.get_packs_control(f)
	for i in res.keys():
		print i, res[i]