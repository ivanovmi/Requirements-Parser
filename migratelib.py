#                   aptitude -F '%p %V' --disable-columns search '~n . ~O Mirantis'


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
    if len(a)>0:
        for i in a:

            if i[0] == '<':
                    status.append(compare_version(version) < compare_version(i[1]))
            elif i[0] == '>':
                    status.append(compare_version(version) > compare_version(i[1]))
            elif i[0] == '==':
                status.append(compare_version(version) == compare_version(i[1]))
            elif i[0] == '>=':
                status.append(compare_version(version) >= compare_version(i[1]))
            elif i[0] == '<=':
                status.append(compare_version(version) <= compare_version(i[1]))
            elif i[0] == '!=':
                status.append(compare_version(version) != compare_version(i[1]))
    if False in status:
        return "The dependency wrong on " + str(status.index(False)+1) + " border", status
    else:
        return 'All OK', status