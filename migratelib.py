#                   aptitude -F '%p %V' --disable-columns search '~n . ~O Mirantis'

import re
import lan
import require_utils
import os
import json

version = re.compile("^[0-9_.:]+")

os.system("aptitude -F '%p %V' --disable-columns search '~n . ~O Mirantis' >> tmp")


def versiontuple(v):
    return tuple(map(int, (v.split("."))))


def compare(version, sets):
    status = []
    a = list(sets)
    a.sort(reverse=True)
    if len(a)>0:
        for i in a:
            if i[0] == '<':
                if versiontuple(version) < versiontuple(i[1]):
                    status.append(True)
                else:
                    status.append(False)
            elif i[0] == '>':
                if versiontuple(version) > versiontuple(i[1]):
                    status.append(True)
                else:
                    status.append(False)
            elif i[0] == '==':
                if versiontuple(version) == versiontuple(i[1]):
                    status.append(True)
                else:
                    status.append(False)
            elif i[0] == '>=':
                if versiontuple(version) >= versiontuple(i[1]):
                    status.append(True)
                else:
                    status.append(False)
            elif i[0] == '<=':
                if versiontuple(version) <= versiontuple(i[1]):
                    status.append(True)
                else:
                    status.append(False)
            elif i[0] == '!=':
                if versiontuple(version) != versiontuple(i[1]):
                    status.append(True)
                else:
                    status.append(False)
    if False in status:
        print "The dependencie wrong on " + str(status.index(False)+1) + " border"
    else:
        print 'All OK'

#compare("1.1.3", [('>', '1.8.0'), ('!=', '1.8.3')])


packages_dict = {}
with open("tmp", "r") as f:
    for line in f:
        package_name = line.split(" ")[0]
        pre_vers = line.split(" ")[1].strip()
        package_vers = version.search(pre_vers)
        if package_vers:
            vers = package_vers.group(0)
        else:
            vers = None
        try:
            if ':' in vers:
                vers = vers.split(':')[1]
        except TypeError:
            pass
        packages_dict[package_name] = vers

try:
    os.remove('tmp')
except OSError:
    pass


# Get global requirements
gerritAccount=lan.login_to_launchpad("mivanov@mirantis.com", "16121814")
req_url = 'https://raw.githubusercontent.com/openstack/requirements/' \
            '{0}/global-requirements.txt'.format("stable/kilo")
r = lan.get_requirements_from_url(req_url, gerritAccount)
rq2 = require_utils.Require.parse_req(r)


control_base_file = open("control-base.json", "r")
control_base = json.load(control_base_file)
for item in rq2:
    for key, basename in control_base.iteritems():
        if item == basename:
            rq2[key]=rq2.pop(item)

for key in packages_dict:
    if key in rq2:
        #print key
        a = list(rq2[key])
        a.sort(reverse=True)
        try:
            print packages_dict[key] + "    ========    " + str(a)#.sort(reverse=True))
            compare(packages_dict[key], rq2[key])
        except TypeError:
            print "None" + "    ========    " + str(list(rq2[key]).sort(reverse=True))