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
        try:
            gerritAccount = lan.login_to_launchpad(launchpad_id, launchpad_pw)
        except:
            print "Sorry, connection wasn't established"
        global_branch_name = ''
        branch_name = ''
        mode = ''
        file_extension = ''
        send = ''

        while mode.lower() not in ['ep', 'req', 'diff',
                                   'migr', 'e', 'r', 'd', 'm']:
            mode = raw_input('Module (Epoch = ep | Requires = req |'
                             ' Diff check = diff | Migrate tool = migr): ')

        if mode.lower() == 'r':
            mode = 'req'
        elif mode.lower() == 'e':
            mode = 'ep'
        elif mode.lower() == 'd':
            mode = 'diff'
        elif mode.lower() == 'm':
            mode = 'migr'

        if mode not in ['diff', 'migr']:
            type_req = raw_input('Scan RPM or DEB (spec | control | '
                                 'empty to pass): ')
            if type_req.lower() not in ["spec", "control"]:
                type_req = ''
        else:
            type_req = ''

        if mode.lower() not in ['diff', 'migr']:
            while branch_name.lower() not in ['master', '8.0',
                                              '7.0', '6.1', '6.0.1']:
                branch_name = raw_input('At the what branch we should '
                                        'check requirements? ')
                if branch_name == 'master':
                    branch = 'master'
                elif branch_name == '8.0':
                    branch = 'openstack-ci/fuel-8.0/liberty'
                elif branch_name == '6.1':
                    branch = 'openstack-ci/fuel-7.0/2015.1.0'
                elif branch_name == '6.1':
                    branch = 'openstack-ci/fuel-6.1/2014.2'
                elif branch_name == '6.0.1':
                    branch = 'openstack-ci/fuel-6.0.1/2014.2'
        else:
            branch = 'master'

        if mode.lower() in ['req', 'migr']:
            while global_branch_name not in ['master', 'juno',
                                             'icehouse', 'kilo', 'liberty']:
                global_branch_name = raw_input('At the what branch we should '
                                               'find global requirements? ')
                if global_branch_name == 'master':
                    global_branch = 'master'
                elif global_branch_name == 'juno':
                    global_branch = 'stable/juno'
                elif global_branch_name == 'icehouse':
                    global_branch = 'stable/icehouse'
                elif global_branch_name == 'kilo':
                    global_branch = 'stable/kilo'
                elif global_branch_name == 'liberty':
                    global_branch = 'stable/liberty'
        else:
            global_branch = None

        if mode != 'migr':
            while file_extension.lower() not in ['pdf', 'html']:
                file_extension = raw_input('With what extension '
                                           'save a file? (PDF or HTML?) ')
        else:
            file_extension = None

        while send.lower() not in ['y', 'n', 'yes', 'no']:
            send = raw_input('Would you like to send a report '
                             'on whether the e-mail? ')
            if send.lower() in ['y', 'yes']:
                email = raw_input('Enter the e-mail: ')
            elif send.lower() in ['n', 'no']:
                email = None

        repo_file = None

        return [launchpad_id, gerritAccount, mode, type_req, branch,
                global_branch, file_extension, send, email, repo_file]

    else:
        try:
            docs = yaml.load_all(config)
            for doc in docs:
                parameters = doc.copy()

            launchpad_id = parameters['launchpad_id']
            launchpad_pw = parameters['launchpad_pw']

            if launchpad_id is None or launchpad_id == '' \
                    or launchpad_pw is None or launchpad_pw == '':
                raise KeyError('launchpad_id or launchpad_pw')

            gerritAccount = lan.login_to_launchpad(launchpad_id, launchpad_pw)
            file_extension = parameters['output_format']
            send = parameters['send_email']

            mode = parameters['mode']

            if mode is None or mode == '':
                raise KeyError('mode')

            if mode not in ['diff', 'd', 'migr', 'm']:
                type_req = parameters['type_req']
            else:
                type_req = ''

            if mode not in ['diff', 'd', 'migr', 'm']:
                branch_name = parameters['branch']
                if branch_name == 'master':
                    branch = 'master'
                elif branch_name == '8.0':
                    branch = 'openstack-ci/fuel-8.0/liberty'
                elif branch_name == '7.0':
                    branch = 'openstack-ci/fuel-7.0/2015.1.0'
                elif branch_name == '6.1':
                    branch = 'openstack-ci/fuel-6.1/2014.2'
                elif branch_name == '6.0.1':
                    branch = 'openstack-ci/fuel-6.0.1/2014.2'
            else:
                branch = 'master'

            if mode in ['req', 'r', 'migr', 'm']:
                global_branch_name = parameters['global_branch']
                if global_branch_name == 'master':
                    global_branch = 'master'
                elif global_branch_name == 'juno':
                    global_branch = 'stable/juno'
                elif global_branch_name == 'icehouse':
                    global_branch = 'stable/icehouse'
                elif global_branch_name == 'kilo':
                    global_branch = 'stable/kilo'
                elif global_branch_name == 'liberty':
                    global_branch = 'stable/liberty'
            else:
                global_branch = None

            repo_file = parameters['file']
            try:
                f = open(repo_file, 'r')
                f.close()
            except IOError:
                repo_file = None
            except TypeError:
                repo_file = None
            else:
                repo_file = parameters['file']

            if mode != 'migr' and file_extension is None \
                    or file_extension == '':
                raise KeyError('output_format')

            if send.lower() in ['yes', 'y']:
                email_to = parameters['email_to']
            elif send.lower() in ['no', 'n']:
                email_to = None

            return [launchpad_id, gerritAccount, mode, type_req, branch,
                    global_branch, file_extension, send, email_to, repo_file]

        except KeyError,  err:
            print str(err)+' not defined'
            raise SystemExit
