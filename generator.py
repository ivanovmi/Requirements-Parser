import os
import lan
import require_utils
import json
import report
from colorama import Fore
import tempfile
import re
import migratelib

tag_dict = {
    'python-barbicanclient': '2.2.1',
    'python-ceilometerclient': '1.0.12',
    'python-cinderclient': '1.1.1',
    'python-glanceclient': '0.15.0',
    'python-heatclient': '0.2.12',
    'python-keystoneclient': '0.11.1',
    'python-openstackclient': '0.4.1',
    'python-saharaclient': '0.7.6',
    'python-swiftclient': '2.3.1',
    'python-neutronclient': '2.3.9',
    'python-novaclient': '2.20.0',
    'python-troveclient': '1.0.7',
    'mistral': '2015.1.0b1',
    'murano-apps': '2014.2',
    'python-mistralclient': '0.1.1',
    'python-muranoclient': '0.5.5',
    'python-congressclient': '1.0.2',
    'glance_store': '0.1.10',
    'oslo.context': '0.1.0',
    'oslo.serialization': '1.2.0',
    'oslo.utils': '1.2.1',
    'oslosphinx': '2.2.0',
    'oslotest': '1.1.0'
}


def request_spec(gerrit_account, repo, branch):
    # List of URLs for spec file
    req_url_spec = ['https://review.fuel-infra.org/gitweb?p=openstack-build/{0}-build.git;'
                    'a=blob_plain;f=rpm/SPECS/{0}.spec;hb=refs/heads/{1}',
                    'https://review.fuel-infra.org/gitweb?p=openstack-build/{0}-build.git;'
                    'a=blob_plain;f=rpm/SPECS/openstack-{0}.spec;hb=refs/heads/{1}',
                    'https://review.fuel-infra.org/gitweb?p=openstack-build/{0}-build.git;'
                    'a=blob_plain;f=rpm/SPECS/python-{0}.spec;hb=refs/heads/{1}']
    idx = 0
    while idx < len(req_url_spec):
        try:
            req_spec = lan.get_requirements_from_url(req_url_spec[idx].format(repo.strip(), branch),
             gerrit_account)
        except KeyError:
            req_spec = None
        idx += 1
        if req_spec is not None:
            break

    if req_spec is None: 
        try:
            req_url_spec = 'https://review.fuel-infra.org/gitweb?p=openstack-build/{0}-build.git;' \
                           'a=blob_plain;f=rpm/SPECS/python-{2}.spec;hb=refs/heads/{1}'.format(repo.strip(),
                                                                        branch, repo.strip().replace('.', '-'))

            req_spec = lan.get_requirements_from_url(req_url_spec, gerrit_account)
        except KeyError:
            print 'Skip ' + repo.strip() + ' RPM repository.'
            req_spec = None

    return req_spec


def request_control(gerrit_account, repo, branch, type):
    # URL for getting changelog file
    req_url_changelog = 'https://review.fuel-infra.org/gitweb?p=openstack-build/{0}-build.git;' \
                        'a=blob_plain;f=debian/{2};hb=refs/heads/{1}'.format(repo.strip(), branch, type)

    try:
        req_control = lan.get_requirements_from_url(req_url_changelog, gerrit_account)
    except KeyError:
        print 'Skip ' + repo.strip() + ' DEB repository.'
        req_control = None

    return req_control


def del_symbol(json_file, n):
    json_file.seek(n, os.SEEK_END)
    json_file.truncate()


def get_req(gerritAccount, req_file, rq2, json_file, branch, type):
    pack_count = 0
    repo_count = 0
    for repo in req_file:
        print '\n' * 3, 'Repos:', repo
        req_url = 'https://review.fuel-infra.org/gitweb?p=openstack/{0}.git;' \
                  'a=blob_plain;f=requirements.txt;hb=refs/heads/{1}'.format(repo.strip(), branch)

        # Check the repo is exist. If not - skipping.
        try:
            r = lan.get_requirements_from_url(req_url, gerritAccount)
        except KeyError:
            print 'Skip ' + repo.strip() + ' repository.'
            continue

        rq1 = require_utils.Require(require_utils.Require.parse_req(r))

        if type:

            if type == "control":
                packs_request = request_control(gerritAccount, repo, branch, "control")
            elif type == "spec":
                packs_request = request_spec(gerritAccount, repo, branch)

            with open("{0}-base.json".format(type), 'r') as b:
                base = json.load(b)

            if packs_request is not None:

                if type == "control":
                    packs_list = require_utils.Require.get_packs_control(packs_request)
                    sector = "Depends:"
                elif type == "spec":
                    packs_list = require_utils.Require.get_packs_spec(packs_request)
                    sector = "Requires:"
                    
                for el in packs_list[sector]:
                    if (base.has_key(el)):
                        rq1.packs.setdefault(base[el], list())
                    else:
                        print "Unknown: " + el
            
        if rq1.packs != {}:
            repo_count += 1
            rq = require_utils.Require.merge(rq1.packs, rq2.packs)
            json_file.write('\t{\n' + '\t' * 2 + json.dumps(repo.strip()) + ': {\n')
            json_file.write('\t' * 2 + '"deps": {\n')
            for key in rq1.packs.keys():

                color_beg = ''
                color_end = ''

                if require_utils.Require.is_changed(rq[key], rq1.packs[key]):
                    # Write to file with bold font and pointer.
                    pack_count += 1
                    color_beg = Fore.RED
                    color_end = Fore.RESET
                    json_file.write('\t' * 3 + json.dumps(''.join('* ' + '**' + key + '**' + ' ' * 8)) +
                                    ':' + json.dumps(''.join([" %s%s;" % x for x in rq[key]])) + ',\n')
                else:
                    # Write to file with standard font.
                    json_file.write('\t' * 3 + json.dumps(''.join(key + ' ' * 8)) + ':' +
                                    json.dumps(''.join([" %s%s;" % x for x in rq[key]])) + ',\n')

                print '{0}{1}{2}:{3}'.format(color_beg, key, color_end, ''.join([" %s%s;" % x for x in rq[key]]))

            # Delete unnecessary comma in the end of dependencies list
            del_symbol(json_file, -2)
            json_file.write('\t' * 2 + '}}},\n')
    if repo_count:
        del_symbol(json_file, -2)
    return pack_count, repo_count


def get_epoch(gerrit_account, req_file, branch, json_file):
    check = False
    for repo in req_file:
        print '\n' * 3, 'Repos:', repo

        req_spec = request_spec(gerrit_account, repo, branch)
        req_control = request_control(gerrit_account, repo, branch, "changelog")

        rpm_epoch = deb_epoch = None

        if req_spec is not None:
            rpm_epoch = require_utils.Require.get_epoch(req_spec)
        if req_control is not None:
            deb_epoch = require_utils.Require.get_epoch(req_control)

        if rpm_epoch or deb_epoch:
            check = True
            json_file.write('\t' * 3 + json.dumps(repo.strip()) + ': {\n')

            if rpm_epoch:
                print "RPM\n" + rpm_epoch + "\n"
                json_file.write('\t' * 4 + '"RPM":' + json.dumps(rpm_epoch) + ',\n')

            if deb_epoch:
                print "DEB\n" + deb_epoch + "\n"
                json_file.write('\t' * 4 + '"DEB": ' + json.dumps(deb_epoch) + ',\n')

            del_symbol(json_file, -2)
            json_file.write('\t' * 3 + '},\n')
    if check:
        del_symbol(json_file, -2)


def diff_check(launchpad_name, json_file, req_file):

    gerrit = launchpad_name

    for repo in req_file:
        repo = repo.strip()
        json_file.write(json.dumps(repo)+':\n')
        print repo

        if 'murano' in repo or 'mistral' in repo or 'congress' in repo:
            git_repo = 'stackforge'
        else:
            git_repo = 'openstack'

        if 'python' in repo and 'client' in repo or 'mistral' in repo or 'apps' in repo \
            or 'store' in repo or 'sphinx' in repo or 'serial' in repo or 'context' in repo \
                or 'utils' in repo or 'test' in repo:
            git_branch = tag_dict[repo]
        else:
            git_branch = 'upstream/stable/juno'

        os.system('./check.sh {0} {1} {2} {3}'.format(gerrit, repo, git_repo, git_branch))

        with open('tmpfile', 'r') as f:

            try:
                last = f.readlines()[-1]
            except IndexError:
                json_file.write('\t{"No changes": "Codes of these components probably have not been changed"},\n')
            else:
                head = last.strip().split(',', 1)[0]
                tail = last.strip().split(',', 1)[1]
                json_file.write('\t{'+json.dumps(head)+': '+json.dumps(tail)+'},\n')
    del_symbol(json_file, -2)
    json_file.write('}')


def migrate(rq2, csvfile):
    version_mask = re.compile("^[0-9_.:]+")
    tmpfile = tempfile.NamedTemporaryFile(delete=False)

    try:
        apt_check = open('/usr/bin/aptitude', 'r')
        apt_check.close()
    except:
        print 'Aptitude is not installed. Please, use apt-get install aptitude before start this tool again'
    else:
        os.system("aptitude -F '%p %V' --disable-columns search '~n . ~O Mirantis' >> {0}".format(tmpfile.name))

    packages_dict = {}

    with open(str(tmpfile.name), 'r') as f:
        for line in f:
            package_name = line.split(' ')[0]
            apt_version = line.split(' ')[1].strip()
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
        os.remove(tmpfile.name)
    except OSError:
        pass

    # change names according base-control rules
    control_base_file = open("control-base.json", "r")
    control_base = json.load(control_base_file)
    for item in rq2:
        for key, basename in control_base.iteritems():
            if item == basename:
                rq2[key]=rq2.pop(item)

    # generate cli output
    for key in packages_dict:
        if key in rq2:

            a = list(rq2[key])
            a.sort(reverse=True)
            if a == []:
                a = migratelib.get_version(key)
                string_format = str(a)
            else:
                string_format = ''.join([" %s%s;" % x for x in rq2[key]])

            result, status = migratelib.compare(packages_dict[key], rq2[key])
            report.generate_csv(csvfile, key, packages_dict[key], string_format, result)
            if result == 'All OK':
                result = Fore.GREEN+'All OK'+Fore.RESET
            else:
                result = Fore.RED+"The dependency wrong on " + str(status.index(False)+1) + " border"+Fore.RESET
            try:
                print key, \
                    '\t', \
                    packages_dict[key] + "  ==================  " + string_format, \
                    result
            except TypeError:
                print '\t', \
                "None  ==================  " + string_format, \
                result
