import require_utils
import pdb
import lan
import sender
import generator
import report as generate_report
import check_diff
import getpass
from os.path import basename

'''
DRAFT:
 - Need to sort project
 - Config from file
 - Forming globals
'''

if __name__ == "__main__":
    try:
        print 'Please, login to gerrit.'
        launchpad_id = raw_input('Login: ')
        launchpad_pw = getpass.getpass()
        #pdb.set_trace()
        pack_count = (0, 0)
        gerritAccount = lan.login_to_launchpad(launchpad_id, launchpad_pw)
        global_branch_name = ''
        branch_name = ''
        mode = ''
        file_extension = ''
        send = ''
        type_req = ''

        while mode.lower() not in ['ep', 'req', 'diff', 'e', 'r', 'd']:
            mode = raw_input('Module (Epoch = ep | Requires = req | Diff check = diff): ')

        type_req = raw_input('Scan RPM or DEB (spec | control | empty to pass): ')
        if type_req.lower() not in ["spec", "control"]:
            type_req = ''

        if mode.lower() not in []:#'diff', 'd']:
            while branch_name.lower() not in ['master', '6.1', '6.0.1']:
                branch_name = raw_input('At the what branch we should check requirements? ')
                if branch_name == 'master':
                    branch = 'master'
                elif branch_name == '6.1':
                    branch = 'openstack-ci/fuel-6.1/2014.2'
                elif branch_name == '6.0.1':
                    branch = 'openstack-ci/fuel-6.0.1/2014.2'

        if mode.lower() in ['req', 'r']:
            while global_branch_name not in ['master', 'juno', 'icehouse']:
                global_branch_name = raw_input('At the what branch we should find global requirements? ')
                if global_branch_name == 'master':
                    global_branch = 'master'
                elif global_branch_name == 'juno':
                    global_branch = 'stable/juno'
                elif global_branch_name == 'icehouse':
                    global_branch = 'stable/icehouse'

        while file_extension.lower() not in ['pdf', 'html']:
            file_extension = raw_input('With what extension save a file? (PDF or HTML?) ')

        while send.lower() not in ['y', 'n', 'yes', 'no']:
            send = raw_input('Would you like to send a report on whether the e-mail? ')
            if send.lower() in ['y', 'yes']:
                email = raw_input('Enter the e-mail: ')
            elif send.lower() in ['n', 'no']:
                pass

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
                        generator.check(launchpad_id.split('@')[0])
                        file_exist_check = False
            except IOError:
                print 'No such file or directory'

        if mode == 'ep':
            json_file.write('\n' + '\t' * 2 + '}' + '\n')
        json_file.write('\t' + '],\n"output_format": "' + file_extension.lower() + '"\n}')
        json_file.close()

        generate_report.generate_output(mode)

        if send.lower() in ['y', 'yes']:
            text = str(pack_count[0]) + ' packages were changed in ' + str(pack_count[1]) + ' repos.'
            sender.send_mail(email, 'Report from ' + sender.cur_time, text, 'report.' + file_extension.lower())
        elif send.lower() in ['n', 'no']:
            raise SystemExit
    except KeyboardInterrupt:
        print 'The process was interrupted by the user'
        raise SystemExit
