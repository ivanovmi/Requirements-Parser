import os
import json
from generator import del_symbol
from subprocess import call

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


def check(laun):
    with open('requirements.json', 'w') as json_file:

        gerrit = laun#'mivanov'
        #json_file.write('[{')
        with open('req', 'r') as repo_file:
            for repo in repo_file:
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
                        json_file.write('\t{"No changes": ""},\n')
                    else:
                        json_file.write('\t{'+json.dumps(last.strip())+': ""},\n')
            del_symbol(json_file, -2)
        #json_file.write('}]')