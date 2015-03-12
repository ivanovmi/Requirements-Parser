import require_utils
import pdb
import os
import lan
import json
import report as generate_report
import sender
import getting


def generate_output():
        # read example JSON
        with open('requirements.json') as jsfile:
            json_data = json.load(jsfile)

        if mode == 'req':
            generate_report.generate_rst(json_data, False)
        elif mode == 'ep':
            generate_report.generate_rst(json_data, True)

if __name__ == "__main__":
    pack_count = 0
    gerritAccount = lan.loginToLaunchpad()
    branch_name = ''
    mode = ''

    while mode not in ['ep', 'req']:
        mode = raw_input('Module (Epoch = ep | Requires = req): ')

    while branch_name not in ['master', '6.1', '6.0.1']:
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

    send = ''
    while send.lower() not in ['y', 'n', 'yes', 'no']:
        send = raw_input('Would you like to send a report on whether the e-mail? ')

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

            if mode == 'req':
                pack_count = getting.get_req(req_file, gerritAccount, rq2, json_file, branch, pack_count)
            else:
                getting.get_epoch(gerritAccount, req_file, branch, json_file)
    if mode == 'ep':
        json_file.write('\n' + '\t' * 2 + '}' + '\n')
    json_file.write('\t'+'],\n"output_format": "'+file_extension.lower()+'"\n}')
    json_file.close()

    generate_output()

    if send.lower() in ['y', 'yes']:
        email = raw_input('Enter the e-mail: ')
        text = str(pack_count) + ' packages were changed'
        sender.send_mail(email, 'Report from '+sender.cur_time, text, 'report.'+file_extension.lower())
    elif send.lower() in ['n', 'no']:
        raise SystemExit