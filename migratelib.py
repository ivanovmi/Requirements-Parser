#                   aptitude -F '%p %V' --disable-columns search '~n . ~O Mirantis'

import re
import lan
import require_utils
import os
import json
from colorama import Fore
import csv

version_mask = re.compile("^[0-9_.:]+")

os.system("aptitude -F '%p %V' --disable-columns search '~n . ~O Mirantis' >> tmp")


def write_header_csv():
    with open('table.csv', 'wb') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(['package_name','GR_lower_bound', 'package_version','GR_upper_bound', 'status'])

write_header_csv()

def compare_version(v):
    return tuple(map(int, (v.split("."))))


def compare(version, sets):
    status = []
    a = list(sets)
    a.sort(reverse=True)
    if len(a)>0:
        for i in a:
            if i[0] == '<':
                if compare_version(version) < compare_version(i[1]):
                    status.append(True)
                else:
                    status.append(False)
            elif i[0] == '>':
                if compare_version(version) > compare_version(i[1]):
                    status.append(True)
                else:
                    status.append(False)
            elif i[0] == '==':
                if compare_version(version) == compare_version(i[1]):
                    status.append(True)
                else:
                    status.append(False)
            elif i[0] == '>=':
                if compare_version(version) >= compare_version(i[1]):
                    status.append(True)
                else:
                    status.append(False)
            elif i[0] == '<=':
                if compare_version(version) <= compare_version(i[1]):
                    status.append(True)
                else:
                    status.append(False)
            elif i[0] == '!=':
                if compare_version(version) != compare_version(i[1]):
                    status.append(True)
                else:
                    status.append(False)
    if False in status:
        return Fore.RED+"The dependency wrong on " + str(status.index(False)+1) + " border"
    else:
        return Fore.GREEN+'All OK'

packages_dict = {}

with open("tmp", "r") as f:
    for line in f:
        package_name = line.split(" ")[0]
        apt_version = line.split(" ")[1].strip()
        version = version_mask.search(apt_version)
        if version:
            package_version = version.group(0)
        else:
            package_version = None
        try:
            if ':' in package_version:
                package_version = package_version.split(':')[1]
        except TypeError:
            pass
        packages_dict[package_name] = package_version

try:
    os.remove('tmp')
except OSError:
    pass


# Get global requirements
gerritAccount=lan.login_to_launchpad('''provide your credentials''')
req_url = 'https://raw.githubusercontent.com/openstack/requirements/' \
            '{0}/global-requirements.txt'.format("stable/kilo")
r = lan.get_requirements_from_url(req_url, gerritAccount)
rq2 = require_utils.Require.parse_req(r)

# change names according base-control rules
control_base_file = open("control-base.json", "r")
control_base = json.load(control_base_file)
for item in rq2:
    for key, basename in control_base.iteritems():
        if item == basename:
            rq2[key]=rq2.pop(item)

#write_header_csv()
# generate cli output
for key in packages_dict:
    if key in rq2:
        a = list(rq2[key])
        a.sort(reverse=True)
        if a == []:
            a = "Any"
            string_format = str(a)
        else:
            string_format = ''.join([" %s%s;" % x for x in rq2[key]])
        print key, '\t', packages_dict[key] + "    ==================    " + string_format, compare(packages_dict[key], rq2[key]), Fore.RESET
 
