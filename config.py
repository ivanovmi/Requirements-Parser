import yaml
import argparse
import lan
import getpass

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--config', dest='config', help='Configuration YAML')
args = parser.parse_args()


def check_config():
    try:
        config = open(args.config, 'r')
    except TypeError:
        print 'Please, login to gerrit.'
        launchpad_id = raw_input('Login: ')
        launchpad_pw = getpass.getpass()
        #pdb.set_trace()
        gerritAccount = lan.login_to_launchpad(launchpad_id, launchpad_pw)
        global_branch_name = ''
        branch_name = ''
        mode = ''
        file_extension = ''
        send = ''
        type_req = ''

        while mode.lower() not in ['ep', 'req', 'diff', 'e', 'r', 'd']:
            mode = raw_input('Module (Epoch = ep | Requires = req | Diff check = diff): ')

        if mode not in ['diff', 'd']:
            type_req = raw_input('Scan RPM or DEB (spec | control | empty to pass): ')
            if type_req.lower() not in ["spec", "control"]:
                type_req = ''
        else:
            type_req = ''

        if mode.lower() not in ['diff', 'd']:
            while branch_name.lower() not in ['master', '6.1', '6.0.1']:
                branch_name = raw_input('At the what branch we should check requirements? ')
                if branch_name == 'master':
                    branch = 'master'
                elif branch_name == '6.1':
                    branch = 'openstack-ci/fuel-6.1/2014.2'
                elif branch_name == '6.0.1':
                    branch = 'openstack-ci/fuel-6.0.1/2014.2'
        else:
            branch = 'master'

        if mode.lower() in ['req', 'r']:
            while global_branch_name not in ['master', 'juno', 'icehouse']:
                global_branch_name = raw_input('At the what branch we should find global requirements? ')
                if global_branch_name == 'master':
                    global_branch = 'master'
                elif global_branch_name == 'juno':
                    global_branch = 'stable/juno'
                elif global_branch_name == 'icehouse':
                    global_branch = 'stable/icehouse'
        else:
            global_branch = None

        while file_extension.lower() not in ['pdf', 'html']:
            file_extension = raw_input('With what extension save a file? (PDF or HTML?) ')

        while send.lower() not in ['y', 'n', 'yes', 'no']:
            send = raw_input('Would you like to send a report on whether the e-mail? ')
            if send.lower() in ['y', 'yes']:
                email = raw_input('Enter the e-mail: ')
            elif send.lower() in ['n', 'no']:
                email = None

        return [launchpad_id, gerritAccount, mode, type_req, branch, global_branch, file_extension, send, email]

    else:
        try:
            docs = yaml.load_all(config)
            for doc in docs:

                launchpad_id = doc['launchpad_id']
                launchpad_pw = doc['launchpad_pw']
                gerritAccount = lan.login_to_launchpad(launchpad_id, launchpad_pw)

                mode = doc['mode']

                if mode not in ['diff', 'd']:
                    type_req = doc['type_req']
                else:
                    type_req = ''

                if mode not in ['diff', 'd']:
                    branch_name = doc['branch']
                    if branch_name == 'master':
                        branch = 'master'
                    elif branch_name == '6.1':
                        branch = 'openstack-ci/fuel-6.1/2014.2'
                    elif branch_name == '6.0.1':
                        branch = 'openstack-ci/fuel-6.0.1/2014.2'
                else:
                    branch = 'master'

                if mode in ['req', 'r']:
                    global_branch_name = doc['global_branch']
                    if global_branch_name == 'master':
                        global_branch = 'master'
                    elif global_branch_name == 'juno':
                        global_branch = 'stable/juno'
                    elif global_branch_name == 'icehouse':
                        global_branch = 'stable/icehouse'
                else:
                    global_branch = None

                file_extension = doc['output_format']

                send = doc['send_email']

                if send.lower() in ['yes', 'y']:
                    email_to = doc['email_to']
                elif send.lower() in ['no', 'n']:
                    email_to = None

            return [launchpad_id, gerritAccount, mode, type_req, branch, global_branch, file_extension, send, email_to]

        except KeyError,  err:
            print str(err)+' not defined'
            raise SystemExit