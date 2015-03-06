__author__ = 'degorenko'

import rst2pdf
import docutils


def generate_rst(json_data):
    f = open("report.rst", "w")

    from email.utils import formatdate
    cur_time = formatdate(timeval=None, localtime=True)

    write_headers(f, '{0} {1}{2}'.format("Dependency checker", cur_time, "\n"), True)
    write_parameters(f, ':{0}: {1}\n'.format("Upstream URL", json_data["upstream_url"]))
    write_parameters(f, ':{0}: {1}\n'.format("Upstream branch", json_data["upstream_branch"]))
    write_parameters(f, ':{0}: {1}\n'.format("MOS gerrit URL", json_data["gerrit_url"]))
    write_parameters(f, ':{0}: {1}\n'.format("MOS gerrit branch", json_data["gerrit_branch"]))

    projects = json_data["projects"]
    for project in projects:
        project_name = project.keys()[0]
        deps = project[project_name]['deps']

        project_reqs = {}
        for key in deps.keys():
            project_reqs[key] = deps[key]

        write_table(f, project_name, project_reqs)

    f.close()

    from subprocess import call
    if json_data["output_format"] == "pdf":
        call(["rst2pdf", "report.rst", "-o", "report.pdf"])
    else:
        call(["rst2html.py", "report.rst", "report.html"])


def write_headers(f, header, main=False):
    header_len = len(header) - 1
    separator = '-'
    if main:
        separator = '='
    head_sep = get_sequence(separator, header_len)
    f.write(header)
    f.write('{0}\n'.format(head_sep))


def write_parameters(f, parameter):
    f.write(parameter)


def get_sequence(separator, count):
    return ''.join([separator for i in xrange(count)])


def get_word_length(dictionary):
    # Default length of table columns -> 'Package name', 'MOS', 'Upstream'
    length = [12, 4]
    for key in dictionary.keys():
        if len(key) > length[0]:
            length[0] = len(key)
        if len(dictionary[key]) > length[1]:
            length[1] = len(dictionary[key])
    return length


def write_table(f, project, requirements):
    word_length = get_word_length(requirements)

    def align(word, num):
        n = word_length[num] - len(word)
        if n > 0:
            m = n / 2
            return '{0}{1}{2}'.format(get_sequence(' ', m),
                                      word,
                                      get_sequence(' ', n - m))
        else:
            return word

    write_headers(f, '\n{0}\n'.format(project))
    write_parameters(f, '+{0}+{1}+\n'.format(get_sequence('-', word_length[0]),
                                                 get_sequence('-', word_length[1])))
    write_parameters(f, '|{0}|{1}|\n'.format(align("Package name", 0),
                                                 align("DEPENDENCIES", 1)))
    write_parameters(f, '+{0}+{1}+\n'.format(get_sequence('=', word_length[0]),
                                                 get_sequence('=', word_length[1])))
    for key in requirements.keys():

        write_parameters(f, '|{0}|{1}|\n'.format(align(key, 0),
                                                     align(requirements[key], 1)))
        write_parameters(f, '+{0}+{1}+\n'.format(get_sequence('-', word_length[0]),
                                                     get_sequence('-', word_length[1])))