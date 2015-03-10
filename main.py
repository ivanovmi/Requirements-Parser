import require_utils
import pdb
import os
import lan
import json
import reporter.report as generate_report
import sender


def generate_output():
        # read example JSON
        with open('requirements.json') as jsfile:
            json_data = json.load(jsfile)
        generate_report.generate_rst(json_data)


if __name__ == "__main__":

    gerritAccount = lan.loginToLaunchpad()
    branch_name = ''
    mode = ''

    while mode not in ['ep', 'req']:
        mode = raw_input('Module (Epoch = ep | Requires = req): ')

    while branch_name not in ['master', '6.1', '6.0.1']:
        #branch_name = 'master'
        branch_name = raw_input('At the what branch we should check requirements? ')
        if branch_name == 'master':
            branch = 'master'
        elif branch_name == '6.1':
            branch = 'openstack-ci/fuel-6.1/2014.2'
        elif branch_name == '6.0.1':
            branch = 'openstack-ci/fuel-6.0.1/2014.2'
    #pdb.set_trace()

    file_extension = ''
    while file_extension.lower() not in ['pdf', 'html']:
        file_extension = raw_input('With what extension save a file? (PDF or HTML?) ')
    json_file = open('requirements.json', 'w')
    json_file.write('{"gerrit_url": "URL",\n'
                    '"gerrit_branch": "branch",\n'
                    '"upstream_url": "URL",\n'
                    '"upstream_branch": "branch",\n')
    json_file.write('\n\t"projects": [\n\t')
    
    if mode == 'req':
        with open('2ndReq', 'r') as f:
            rq2 = require_utils.Require(require_utils.Require.parse_req(f))
    else:
        json_file.write('\t{\n')

    with open('req', 'r') as req_file:
        pack_count = 0
        for repo in req_file:
            print '\n'*3, 'Repos:', repo

            if mode == 'req':
                req_url = 'https://review.fuel-infra.org/gitweb?p=openstack/{0}.git;a=blob_plain;f=requirements.txt;hb=refs/heads/{1}'.format(repo.strip(), branch)
                # Check the repo is exist. If not - skipping.
                try:
                    r = lan.getRequirementsFromUrl(req_url, gerritAccount)
                except KeyError:
                    print 'Skip ' + repo.strip() + ' repository.'
                    continue
                rq1 = require_utils.Require(require_utils.Require.parse_req(r))
                if rq1.packs != {}:
                    rq = require_utils.Require.merge(rq1.packs, rq2.packs)
                    json_file.write('\t{\n' + '\t'*2+json.dumps(repo.strip())+': {\n')
                    json_file.write('\t'*2+'"deps": {\n')
                    for key in rq1.packs.keys():
                        boldBeg = ''
                        boldEnd = ''
                        if require_utils.Require.is_changed(rq[key], rq1.packs[key]):
                            # Write to file with bold font and pointer.
                            pack_count += 1
                            boldBeg = '\033[1m'
                            boldEnd = '\033[0m'
                            json_file.write('\t'*3+json.dumps(''.join('* '+'**'+key+'**'+' '*8))+':'+json.dumps(''.join([" %s%s;" % x for x in rq[key]]))+',\n')
                        else:
                            # Write to file with standard font.
                            json_file.write('\t'*3+json.dumps(''.join(key+' '*8))+':'+json.dumps(''.join([" %s%s;" % x for x in rq[key]]))+',\n')
                        print '{0}{1}{2}:{3}'.format(boldBeg, key, boldEnd, ''.join([" %s%s;" % x for x in rq[key]]))
                    # Delete unnecessary comma in the end of dependencies list
                    json_file.seek(-2, os.SEEK_END)
                    json_file.truncate()
                    json_file.write('\t'*2+'}}},\n')
                else:
                    continue
            else:
                req_url_control = 'https://review.fuel-infra.org/gitweb?p=openstack-build/{0}-build.git;a=blob_plain;f=debian/changelog;hb=refs/heads/{1}'.format(repo.strip(), branch)

                idx = 0
                req_url_spec = ['https://review.fuel-infra.org/gitweb?p=openstack-build/{0}-build.git;a=blob_plain;f=rpm/SPECS/{0}.spec;hb=refs/heads/{1}',
                                'https://review.fuel-infra.org/gitweb?p=openstack-build/{0}-build.git;a=blob_plain;f=rpm/SPECS/openstack-{0}.spec;hb=refs/heads/{1}',
                                'https://review.fuel-infra.org/gitweb?p=openstack-build/{0}-build.git;a=blob_plain;f=rpm/SPECS/python-{0}.spec;hb=refs/heads/{1}']

                while idx < len(req_url_spec):
                    try:
                        req_spec = lan.getRequirementsFromUrl(req_url_spec[idx].format(repo.strip(), branch), gerritAccount)
                    except KeyError:
                        req_spec = None
                    idx += 1
                    if not req_spec is None:
                        break

                if req_spec is None:
                    try:
                        req_url_spec = 'https://review.fuel-infra.org/gitweb?p=openstack-build/{0}-build.git;a=blob_plain;f=rpm/SPECS/python-{2}.spec;hb=refs/heads/{1}'.format(repo.strip(), branch, repo.strip().replace('.', '-'))
                        req_spec = lan.getRequirementsFromUrl(req_url_spec, gerritAccount)
                    except KeyError:
                        print 'Skip ' + repo.strip() + ' RPM repository.'
                        req_spec = None

                try:
                    req_control = lan.getRequirementsFromUrl(req_url_control, gerritAccount)
                except KeyError:
                    print 'Skip ' + repo.strip() + ' DEB repository.'
                    req_control = None

                rpm_epoch = deb_epoch = None
                if not req_spec is None:
                    rpm_epoch = require_utils.Require.get_epoch(req_spec)
                if not req_control is None:
                    deb_epoch = require_utils.Require.get_epoch(req_control)

                if rpm_epoch or deb_epoch:
                    json_file.write('\t' * 2 + json.dumps(repo.strip()) + ': {\n')

                    if rpm_epoch:
                        print "RPM\n" + rpm_epoch + "\n"
                        json_file.write('\t' * 3 + '"RPM":' + json.dumps(rpm_epoch) + ',\n')

                    if deb_epoch:
                        print "DEB\n" + deb_epoch + "\n"
                        json_file.write('\t' * 3 + '"DEB":' + json.dumps(deb_epoch) + '\n')

                    json_file.write('\t' * 2 + '},\n')

        # Delete unnecessary comma in the end of project list
        json_file.seek(-2, os.SEEK_END)
        json_file.truncate()
    if mode == 'ep':
        json_file.write('\n' + '\t' * 2 + '}' + '\n')
    json_file.write('\t'+'],\n"output_format": "'+file_extension.lower()+'"\n}')
    json_file.close()
    generate_output()

    send = ''
    while send.lower() not in ['y', 'n', 'yes', 'no']:
        send = raw_input('Would you like to send a report on whether the e-mail? ')
        if send.lower() in ['y', 'yes']:
            email = raw_input('Enter the e-mail: ')
            text = str(pack_count) + ' packages were changed'
            sender.send_mail(email, 'Report from '+sender.cur_time, text, 'report.'+file_extension.lower())
        elif send.lower() in ['n', 'no']:
            raise SystemExit
    '''
    os.system("./emailSend.sh {0} "'"{1}"'"".format('mivanov@mirantis.com', 'report.' + file_extension.lower()))
    for i in rq1.packs.items():
        print i
    for key in rq1.packs.keys():
        print "{0} {1}".format(key, rq[key])'''