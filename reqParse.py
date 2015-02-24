import re

packageName = re.compile("[a-zA-Z0-9-_]+")
packageEq = re.compile("(>=|<=|>|<|==|!=)+")
packageVers = re.compile("[\d.]+")

def parseReq(input):
	res = dict([])
	with open(input, 'r') as f:
		for line in f:
			resName = packageName.search(line)
			resEq = packageEq.findall(line)
			it = next(re.finditer('>=|<=|>|<|==|!=', line), None)
			if it:
				resVers = packageVers.findall(line[it.start():])
			if resName:
				name = resName.group(0)
				if not res.has_key(name):
					res[name] = []
					for idx, sign in enumerate(resEq):
						res[name].append((sign, resVers[idx]))
	return res