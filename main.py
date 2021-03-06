import require_utils
import socket
import lan
import sender
import generator
import report as generate_report
import os
from os.path import basename
import config

'''
DRAFT:
 - Forming globals
'''

if __name__ == "__main__":
    try:
        pack_count = (0, 0)
        try:
            parameters_list = config.check_config()
        except UnboundLocalError, err:
            print str(err).split(' ')[2]+' not defined'
            raise SystemExit

        launchpad_id = parameters_list[0]
        gerritAccount = parameters_list[1]
        mode = parameters_list[2]
        type_req = parameters_list[3]
        branch = parameters_list[4]
        global_branch = parameters_list[5]
        file_extension = parameters_list[6]
        send = parameters_list[7]
        email = parameters_list[8]
        file_with_repo = parameters_list[9]

        if mode != 'migr':
            json_file = open('requirements.json', 'w')
            generate_report.generate_header_rst(json_file, branch)
        else:
            csvfile = open('table '+sender.cur_time+'.csv', 'w')
            generate_report.generate_header_csv(csvfile)

        if mode in ['req', 'migr']:
            req_url = 'https://raw.githubusercontent.com/openstack/requirements/' \
                      '{0}/global-requirements.txt'.format(global_branch)
            r = lan.get_requirements_from_url(req_url, gerritAccount)
            if mode == 'req':
                rq2 = require_utils.Require(require_utils.Require.parse_req(r))
            elif mode == 'migr':
                rq2 = require_utils.Require.parse_req(r)
        else:
            json_file.write('\t{\n')

        file_exist_check = False
        if mode != 'migr':
            if file_with_repo:
                req_file = open(file_with_repo, 'r')
            else:
                try:
                    req_file = open('repos_name', 'r')
                except IOError:
                    file_exist_check = True

        while file_exist_check:
            repo_file = raw_input('Enter the file with repos name: ')
            try:
                req_file = open(basename(repo_file), 'r')
                file_exist_check = False
            except IOError:
                print 'No such file or directory'

        if mode == 'req':
            pack_count = generator.get_req(gerritAccount, req_file,
                                           rq2, json_file, branch, type_req)
        elif mode == 'ep':
            generator.get_epoch(gerritAccount, req_file, branch, json_file)
        elif mode == 'migr':
            generator.migrate(rq2, csvfile)
            csvfile.close()
        else:
            generator.diff_check(launchpad_id.split('@')[0],
                                 json_file, req_file)

        if mode == 'ep':
            json_file.write('\n' + '\t' * 2 + '}' + '\n')

        if mode != 'migr':
            json_file.write('\t' + '],\n"output_format": "' +
                            file_extension.lower() + '"\n}')
            json_file.close()

        if mode != 'migr':
            filename = generate_report.generate_output(mode)
        else:
            filename = generate_report.generate_output(mode, csvfile.name)

        un_file = ['report.rst', 'tmpfile', 'requirements.json']

        for i in un_file:
            try:
                os.remove(i)
            except OSError:
                pass

        if send.lower() in ['y', 'yes']:
            text = str(pack_count[0]) + ' packages were changed in ' +\
                str(pack_count[1]) + ' repos.'
            try:
                sender.send_mail(email, 'Report from ' + sender.cur_time,
                                 text, filename)
            except socket.error:
                print 'Ooops. I did not know, whats wrong. ' \
                      'It is with socket, I think'
        elif send.lower() in ['n', 'no']:
            raise SystemExit
        pass
    except KeyboardInterrupt:
        print '\nThe process was interrupted by the user'
        raise SystemExit
