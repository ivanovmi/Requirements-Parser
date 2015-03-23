import require_utils
import pdb
import lan
import sender
import generator
import report as generate_report
import getpass
import os
from os.path import basename
import config

'''
DRAFT:
 - Need to sort project
 - Config from file
 - Forming globals
'''

if __name__ == "__main__":
    try:
        pack_count = (0, 0)
        parameters_list = config.check_config()

        launchpad_id = parameters_list[0]
        gerritAccount = parameters_list[1]
        mode = parameters_list[2]
        type_req = parameters_list[3]
        branch = parameters_list[4]
        global_branch = parameters_list[5]
        file_extension = parameters_list[6]
        send = parameters_list[7]
        email = parameters_list[8]

        json_file = open('requirements.json', 'w')

        generate_report.generate_header(json_file, branch)

        if mode == 'req':
            req_url = 'https://raw.githubusercontent.com/openstack/requirements/{0}/global-requirements.txt'.format(global_branch)
            r = lan.get_requirements_from_url(req_url, gerritAccount)
            rq2 = require_utils.Require(require_utils.Require.parse_req(r))
        else:
            json_file.write('\t{\n')

        try:
            f = open('repos_name', 'r')
        except IOError:
            file_exist_check = True
        while file_exist_check:
            repo_file = raw_input('Enter the file with repos name: ')
            try:
                with open(basename(repo_file), 'r') as req_file:
                    if mode == 'req':
                        pack_count = generator.get_req(gerritAccount, req_file, rq2, json_file, branch, type_req)
                        file_exist_check = False
                    elif mode == 'ep':
                        generator.get_epoch(gerritAccount, req_file, branch, json_file)
                        file_exist_check = False
                    else:
                        generator.diff_check(launchpad_id.split('@')[0], json_file, req_file)
                        file_exist_check = False
            except IOError:
                print 'No such file or directory'

        if mode == 'ep':
            json_file.write('\n' + '\t' * 2 + '}' + '\n')
        json_file.write('\t' + '],\n"output_format": "' + file_extension.lower() + '"\n}')
        json_file.close()

        filename = generate_report.generate_output(mode)

        un_file = ['report.rst', 'tmpfile', 'requirements.json']
        try:
            for i in un_file:
                os.remove(i)
        except OSError:
            pass

        if send.lower() in ['y', 'yes']:
            text = str(pack_count[0]) + ' packages were changed in ' + str(pack_count[1]) + ' repos.'
            sender.send_mail(email, 'Report from ' + sender.cur_time, text, filename)
        elif send.lower() in ['n', 'no']:
            raise SystemExit
        pass
    except KeyboardInterrupt:
        print '\nThe process was interrupted by the user'
        raise SystemExit
