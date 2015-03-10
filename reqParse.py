import re

packageName = re.compile("[a-zA-Z0-9-_.]+")
packageEq = re.compile("(>=|<=|>|<|==|!=)+")
packageVers = re.compile("[\d.]+")

#This function is for parsing requirements file to special format: [(sign, version),..., (sign, version)].
#Output example: { "pbr" : [ (">=", "0.6"), ("!=", "0.7"), ("<", "1.0")] }
def parseReq(inp):
    res = dict()
    for line in inp:
        if line == '' or line[0] == '#':
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