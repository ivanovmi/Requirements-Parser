import re

packageName = re.compile("[a-zA-Z-_]+")
packageEq = re.compile("(>=|<=|>|<|==|!=)+")
packageVers = re.compile("[\d.]+")

with open('input', 'r') as f:
	for i in f:
		resName = packageName.search(i)
		resEq = packageEq.findall(i)
		resVers = packageVers.findall(i)
		if resName:
			print resName.group(0)
			print resEq
			print resVers