import re

packageName = re.compile("[a-zA-Z0-9-_.]+")
packageEq = re.compile("(>=|<=|>|<|==|!=)+")
packageVers = re.compile("[\d.]+")

def parseReq(input):
	res = dict()
	with open(input, 'r') as f:
		for line in f:
			if line[0] == '#':
				continue
			resName = packageName.search(line)
			resEq = packageEq.findall(line)
			it = next(re.finditer('>=|<=|>|<|==|!=', line), None)
			if it:
				resVers = packageVers.findall(line[it.start():])
			if resName:
				name = resName.group(0)
				if not res.has_key(name):
					res[name] = set()
					for idx, sign in enumerate(resEq):
						res[name].add((sign, resVers[idx]))
	return res