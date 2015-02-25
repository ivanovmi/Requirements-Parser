class Require:

	packs = dict()

	def __init__(self, req):
		self.packs = req
		for el in self.packs.keys():
			self.packs[el] = sorted(self.packs[el], key = lambda tup: tup[1])

	@staticmethod
	def merge(req1, req2):
		req = dict(req1.items() + req2.items())

		for el in req1.keys():
			req[el] = set(req[el]) | set(req1[el])
			res = filter(lambda x: x[0] == '!=', req[el])
			req[el] = sorted(req[el], key = lambda tup: tup[1])
			for i in reversed(req[el]):
				if i[0] in ['>', '>=']:
					res.append(i)
					break
			for i in req[el]:
				if i[0] in ['<', '<=']:
					res.append(i)
					break
			req[el] = res

		return req