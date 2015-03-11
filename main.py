import pdb
import os
import sender
import lan
import require_utils
import json
import gens


if __name__ == "__main__":
    #pdb.set_trace()

    gerritAccount = lan.loginToLaunchpad()
    branch_name = ''
    mode = ''

    while mode not in ['epoch', 'req']:
        mode = raw_input('Module (Epoch = epoch | Requires = req): ')

    while branch_name not in ['master', '6.1', '6.0.1']:
        #branch_name = 'master'
        branch_name = raw_input('Branch for checking: ')
        if branch_name == 'master':
            branch = 'master'
        elif branch_name == '6.1':
            branch = 'openstack-ci/fuel-6.1/2014.2'
        elif branch_name == '6.0.1':
            branch = 'openstack-ci/fuel-6.0.1/2014.2'

    file_extension = ''
    while file_extension.lower() not in ['pdf', 'html']:
        file_extension = raw_input('Output file extention (PDF or HTML): ')

    if mode == 'req':
        with open('2ndReq', 'r') as f:
            rq2 = require_utils.Require(require_utils.Require.parse_req(f))

    gens.generate_json(mode, branch, file_extension, gerritAccount)

    if mode == 'epoch':
        gens.generate_output(True)
    else:
        gens.generate_output()

    send = ''
    while send.lower() not in ['y', 'n', 'yes', 'no']:
        send = raw_input('Would you like to send a report on whether the e-mail? ')
        if send.lower() in ['y', 'yes']:
            email = raw_input('Enter the e-mail: ')
            text = str(pack_count) + ' packages were changed'
            sender.send_mail(email, 'Report from ' + sender.cur_time, text, 'report.' + file_extension.lower())
        elif send.lower() in ['n', 'no']:
            raise SystemExit