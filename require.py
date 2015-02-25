class Require:

	packs = dict()

	def __init__(self, req):
		self.packs = req
		for el in self.packs.keys():
			self.packs[el] = sorted(self.packs[el], key = lambda x: x[1])

	@staticmethod
	def merge(req1, req2):
		req = dict(req1.items() + req2.items())

		for el in req1.keys():
			req[el] = set(req[el]) | set(req1[el])
			req[el] = sorted(req[el], key = lambda x: x[1])

			pred = None
			idx = 0
			while idx < len(req[el]):
				if pred != None:
					if req[el][idx][1] == pred[1]:
						if req[el][idx][0] == '!=':
							req[el][idx], req[el][idx - 1] = req[el][idx - 1], req[el][idx]
						if req[el][idx][0] in ['>', '<']:
							req[el].pop(idx - 1)
						elif req[el][idx][0] in ['>=', '<=']:
							if req[el][idx - 1][0] != '!=':
								req[el].pop(idx)
							else:
								req[el][idx] = (req[el][idx][0][:1], req[el][idx][1])
								req[el].pop(idx - 1)
						idx -= 1
				pred = req[el][idx]
				idx += 1

			res = filter(lambda x: x[0] == '!=', req[el])
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