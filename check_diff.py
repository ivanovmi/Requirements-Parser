import os
import json
from subprocess import call


with open('new.json', 'w') as json_file:

    gerrit = 'mivanov'

    with open('req', 'r') as repo_file:
        for repo in repo_file:
            repo = repo.strip()
            print repo
            os.system('./check.sh {0} {1}'.format(gerrit, repo))
            with open('tmpfile', 'r') as f:
                last = f.readlines()[-1]
                #all_changes = f.re
                json_file.write(json.dumps(last)+': ""')#+json.dumps)
        '''
        call(['git', 'clone', 'ssh://{0}@review.fuel-infra.org:29418/openstack/{1}'.format(gerrit, repo),
              '&&', 'cd', repo,
              '&&', 'git', 'remote', 'add', 'upstream', 'https://github.com/openstack/{0}.git'.format(repo),
              '&&', 'git', 'remote', 'update',
              '&&', 'git', 'diff', '--stat', 'upstream/stable/juno', 'origin/openstack-ci/fuel-6.1/2014.2',
              '&&', 'cd', '..',
              '&&', 'rm', '-rf', repo])

        print '----------------CLONE----------------------------------------------------------------------'
        call(['git', 'clone', 'ssh://{0}@review.fuel-infra.org:29418/openstack/{1}'.format(gerrit, repo)])
        print '------------------------CHANGE DIRECTORY---------------------------------------------------'
        call(['cd', repo])
        print '---------------------REMOTE ADD UPSTERAM---------------------------------------------------'
        call(['git', 'remote', 'add', 'upstream', 'https://github.com/openstack/{0}.git'.format(repo)])
        print '----------------------REMOTE UPDATE--------------------------------------------------------'
        call(['git', 'remote', 'update'])
        print '-----------------------------DIFF----------------------------------------------------------'
        call(['git', 'diff', '--stat', 'upstream/stable/juno', 'origin/openstack-ci/fuel-6.1/2014.2'])
        print '--------------------------------EXIT FROM DIR----------------------------------------------'
        call(['cd', '..'])
        print '-------------------------------REMOVE DIR--------------------------------------------------'
        call(['rm', '-rf', repo])'''