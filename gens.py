import lan
import require_utils
import json
import os
import reporter.report as generate_report

#Generates rst from json
def generate_output(epoch = False):
        # read example JSON
        with open('out.json') as jsfile:
            json_data = json.load(jsfile)
        generate_report.generate_rst(json_data, epoch)

#Generates json according input data
def generate_json(mode, branch, file_extension, gerritAccount):
    #Delete unnecessary commas
    def del_commas(n):
        json_file.seek(n, os.SEEK_END)
        json_file.truncate()

    json_file = open('out.json', 'w')
    json_file.write('{"gerrit_url": "URL",\n'
                    '"gerrit_branch": "branch",\n'
                    '"upstream_url": "URL",\n'
                    '"upstream_branch": "branch",\n')
    json_file.write('\n\t"projects": [\n')

    with open('req', 'r') as req_file:
        pack_count = 0
        for repo in req_file:
            print '\n' * 3, 'Repos:', repo

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
                    json_file.write('\t{\n' + '\t' * 2 + json.dumps(repo.strip()) + ': {\n')
                    json_file.write('\t' * 2 + '"deps": {\n')
                    for key in rq1.packs.keys():
                        boldBeg = ''
                        boldEnd = ''
                        if require_utils.Require.is_changed(rq[key], rq1.packs[key]):
                            # Write to file with bold font and pointer.
                            pack_count += 1
                            boldBeg = '\033[1m'
                            boldEnd = '\033[0m'
                            json_file.write('\t' * 3 + json.dumps(''.join('* ' + '**' + key + '**' + ' '*8)) + ':' + json.dumps(''.join([" %s%s;" % x for x in rq[key]])) + ',\n')
                        else:
                            # Write to file with standard font.
                            json_file.write('\t' * 3 + json.dumps(''.join(key + ' ' * 8)) + ':' + json.dumps(''.join([" %s%s;" % x for x in rq[key]])) + ',\n')
                        print '{0}{1}{2}:{3}'.format(boldBeg, key, boldEnd, ''.join([" %s%s;" % x for x in rq[key]]))

                    del_commas(-2)
                    json_file.write('\t' * 2 + '}}},\n')
                else:
                    continue
            else:
                #URL for getting changelog file
                req_url_changelog = 'https://review.fuel-infra.org/gitweb?p=openstack-build/{0}-build.git;a=blob_plain;f=debian/changelog;hb=refs/heads/{1}'.format(repo.strip(), branch)

                idx = 0
                #List of URLs for spec file 
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
                    req_control = lan.getRequirementsFromUrl(req_url_changelog, gerritAccount)
                except KeyError:
                    print 'Skip ' + repo.strip() + ' DEB repository.'
                    req_control = None

                rpm_epoch = deb_epoch = None
                if not req_spec is None:
                    rpm_epoch = require_utils.Require.get_epoch(req_spec)
                if not req_control is None:
                    deb_epoch = require_utils.Require.get_epoch(req_control)

                if rpm_epoch or deb_epoch:
                    json_file.write('\t' + '{\n' + '\t' * 2 + json.dumps(repo.strip()) + ': {')

                    if rpm_epoch:
                        print "RPM\n" + rpm_epoch + "\n"
                        json_file.write('\n' + '\t' * 3 + '"RPM":' + json.dumps(rpm_epoch) + ',')

                    if deb_epoch:
                        print "DEB\n" + deb_epoch + "\n"
                        json_file.write('\n' + '\t' * 3 + '"DEB":' + json.dumps(deb_epoch) + ',')

                    del_commas(-1)
                    json_file.write('\n' + '\t' * 2 + '}\n' + '\t' + '},\n')

        del_commas(-2)

    json_file.write('\t'+'],\n"output_format": "' + file_extension.lower() + '"\n}')
    json_file.close()