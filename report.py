__author__ = 'degorenko'
import json
import os
import csv

from email.utils import formatdate
cur_time = formatdate(timeval=None, localtime=True)


def generate_output(mode, file=None):
        # read example JSON
        if mode != 'migr':
            with open('requirements.json') as json_file:
                json_data = json.load(json_file)

        if mode == 'req':
            filename = generate_rst(json_data, False)
        elif mode == 'ep':
            filename = generate_rst(json_data, True)
        elif mode == 'diff':
            filename = generate_rst(json_data, True)
        elif mode == 'migr':
            filename = file

        return filename


def generate_header_csv(csvfile):
    csvwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    csvwriter.writerow(['Package name', 'Package version', 'Requirements', 'Status'])


def generate_csv(csvfile, package_name, version, vers_req, result):

    csvwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    csvwriter.writerow([package_name, version, vers_req, result])


def generate_header_rst(json_file, branch):
    json_file.write('{"gerrit_branch": "' + str(branch) + '",\n')
    json_file.write('\n\t"projects": [\n\t')


def generate_rst(json_data, epoch):
    f = open("report.rst", "w")

    write_headers(f, '{0} {1}{2}'.format("Dependency checker",
                                         cur_time, "\n"), True)
    write_parameters(f, ':{0}: {1}\n'.format("MOS gerrit branch",
                                             json_data["gerrit_branch"]))

    def req_rst(project_name):
        deps = project[project_name]['deps']

        project_reqs = {}
        for key in deps.keys():
            project_reqs[key] = deps[key]

        write_table(f, project_name, project_reqs, False)

    def epoch_rst(project_name):
        project_epoch = project[project_name]

        write_table(f, project_name, project_epoch, True)

    projects = json_data["projects"]
    for project in projects:
        project_name = project.keys()
        project_name.sort()

        for i in project_name:

            if epoch:
                epoch_rst(i)
            else:
                req_rst(i)

    f.close()

    from subprocess import call
    if json_data["output_format"] == "pdf":
        filename = 'report '+cur_time+'.pdf'
        call(["rst2pdf", "report.rst", "-o", filename])
    elif json_data["output_format"]:
        filename = 'report.html'
        os.system('rst2html.py report.rst {0}'.format(filename))

    return filename


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
    # Default length of table columns -> 'Package name', 'DEPENDENCIES'
    length = [12, 15]
    for key in dictionary.keys():
        if len(key) > length[0]:
            length[0] = len(key)
        if len(dictionary[key]) > length[1]:
            length[1] = len(dictionary[key])
    return length


def write_table(f, project, requirements, epoch):
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

    def write(clmn1, clmn2):
        write_headers(f, '\n{0}\n'.format(project))
        write_parameters(f, '+{0}+{1}+\n'.format(get_sequence('-', word_length[0]),
                                                 get_sequence('-', word_length[1])))
        write_parameters(f, '|{0}|{1}|\n'.format(align(clmn1, 0),
                                                 align(clmn2, 1)))
        write_parameters(f, '+{0}+{1}+\n'.format(get_sequence('=', word_length[0]),
                                                 get_sequence('=', word_length[1])))

        for key in requirements.keys():
            write_parameters(f, '|{0}|{1}|\n'.format(align(key, 0),
                                                     align(requirements[key], 1)))
            write_parameters(f, '+{0}+{1}+\n'.format(get_sequence('-', word_length[0]),
                                                     get_sequence('-', word_length[1])))

    if epoch:
        write("Repo type", "Epoch")
    else:
        write("Package name", "DEPENDENCIES")