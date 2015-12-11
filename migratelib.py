#              aptitude -F '%p %V' --disable-columns search '~n . ~O Mirantis'


def compare_version(v):
    try:
        return tuple(map(int, (v.split("."))))
    except ValueError:
        pass
    except AttributeError:
        pass


def compare(version, sets):
    # global status
    status = []
    a = list(sets)
    a.sort(reverse=True)
    if len(a) > 0:
        for i in a:

            if i[0] == '<':
                    status.append(compare_version(version)
                                  < compare_version(i[1]))
            elif i[0] == '>':
                    status.append(compare_version(version)
                                  > compare_version(i[1]))
            elif i[0] == '==':
                status.append(compare_version(version)
                              == compare_version(i[1]))
            elif i[0] == '>=':
                status.append(compare_version(version)
                              >= compare_version(i[1]))
            elif i[0] == '<=':
                status.append(compare_version(version)
                              <= compare_version(i[1]))
            elif i[0] == '!=':
                status.append(compare_version(version)
                              != compare_version(i[1]))
    if False in status:
        return "The dependency wrong on " + str(status.index(False)+1) + \
               " border", status
    else:
        return 'All OK', status


def get_version(package_name):
    import os
    import tempfile
    import subprocess

    if package_name.startswith('python-') and package_name.endswith('client'):
        pass
    elif package_name.startswith('python-'):
        package_arr = package_name.split('-')
        package_arr.remove('python')
        if len(package_arr) > 1:
            package_name = '-'.join(package_arr)
        else:
            package_name = package_arr[0]

    tmpfile = tempfile.NamedTemporaryFile(delete=False)

    # os.system('easy_install --dry-run --user {0} >> {1}'.
    # format(package_name, tmpfile.name))
    try:
        easy_install_check = open('/usr/local/bin/easy_install', 'r')
        easy_install_check.close()
    except:
        print 'easy_install is not installed. ' \
              'Please, use apt-get install python-setuptools ' \
              'before start this tool again'
        raise SystemExit
    else:
        command = 'easy_install --dry-run --user '\
                  + package_name + ' >> ' + tmpfile.name

    stdout = open('/dev/null', "w")
    stderr = open('/dev/null', "w")
    subprocess.call(command, shell=True, stdout=stdout, stderr=stderr)

    with open(tmpfile.name, 'r') as f:
        for i in f:
            if i.startswith('Best'):
                version = i.split(' ')[3]
    f.close()
    os.remove(tmpfile.name)

    return version.strip()
