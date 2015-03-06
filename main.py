import reqParse
import require
import pdb
import os
import lan
import json
import reporter.report as generate_report


def generate_output():
        # read example JSON
        with open("requirements.json") as jsfile:
            json_data = json.load(jsfile)
        generate_report.generate_rst(json_data)


def is_changed(a, b):
    try:
        signList_a, verList_a = zip(*a)
    except ValueError:
        signList_a, verList_a = "", ""
    try:
        signList_b, verList_b = zip(*b)
    except ValueError:
        signList_b, verList_b = "", ""
    if set(signList_a) != set(signList_b) or set(verList_a) != set(verList_b):
        return True
    else:
        return False

if __name__ == "__main__":
    branch_name = ''
    while branch_name not in ['master', '6.1', '6.0.1']:
        branch_name = 'master'
        #branch_name = raw_input("At the what branch we should check requirements? ")
        if branch_name == 'master':
            branch = 'master'
        elif branch_name == '6.1':
            branch = 'openstack-ci/fuel-6.1/2014.2'
        elif branch_name == '6.0.1':
            branch = 'openstack-ci/fuel-6.0.1/2014.2'
    #pdb.set_trace()
    gerritAccount = lan.loginToLaunchpad()
    json_file = open('requirements.json', 'w')
    json_file.write('{"gerrit_url": "URL",\n'
                    '"gerrit_branch": "branch",\n'
                    '"upstream_url": "URL",\n'
                    '"upstream_branch": "branch",\n')
    json_file.write('\n\t"projects": [\n\t')
    with open("2ndReq", 'r') as f:
        rq2 = require.Require(reqParse.parseReq(f))
    with open('req', 'r') as req_file:
        for repo in req_file:
            print '\n'*3, "Repos:", repo
            req_url = 'https://review.fuel-infra.org/gitweb?p=openstack/' + repo.strip() + '.git;a=blob_plain;f=requirements.txt;hb=refs/heads/' + branch
            r = lan.getRequirementsFromUrl(req_url, gerritAccount)
            rq1 = require.Require(reqParse.parseReq(r))
            rq = require.Require.merge(rq1.packs, rq2.packs)
            json_file.write('\t{\n'+'\t'*2+json.dumps(repo.strip())+': {\n')
            json_file.write('\t'*2+'"deps": {\n')
            for key in rq1.packs.keys():
                boldBeg = ""
                boldEnd = ""
                if is_changed(rq[key], rq1.packs[key]):
                    boldBeg = "\033[1m"
                    boldEnd = "\033[0m"
                    json_file.write('\t'*3+json.dumps('**'+key+'**')+':'+json.dumps(''.join([" %s%s;" % x for x in rq[key] ]))+',\n')
                else:
                    json_file.write('\t'*3+json.dumps(key)+':'+json.dumps(''.join([" %s%s;" % x for x in rq[key] ]))+',\n')
                print "{0}{1}{2}:{3}".format(boldBeg, key, boldEnd, ''.join([" %s%s;" % x for x in rq[key]]))
            json_file.seek(-2, os.SEEK_END)
            json_file.truncate()
            json_file.write('\t'*2+'}}},\n')
        json_file.seek(-2, os.SEEK_END)
        json_file.truncate()
    json_file.write('\t'+'],\n"output_format": "pdf"\n}')
    json_file.close()
    generate_output()
    #os.system("./emailSend.sh {0} "'"{1}"'"".format("asteroid566@gmail.com", rq.items()))
    #for i in rq1.packs.items():
    #	print i
    # #for key in rq1.packs.keys():
    #	print "{0} {1}".format(key, rq[key])