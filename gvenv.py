#!/usr/bin/env python3.5
# imports
import sys
import os
import os.path as path
import shutil
from venv import EnvBuilder

# my imports
from configuration import Configuration

USAGES = ('new', '--help', 'activate', 'defaultconf', 'show', 'install')


def check_installation():
    '''
    check if the program is correctly installed
    '''
    c = Configuration()

    is_correct = True
    if not os.path.exists(c.conf_dir_name):
        is_correct = False

    return is_correct


def install(p_name):
    '''
    installation of gvenv:
        - gen the directory of gvenv and all the configuration files
        - add gvenv to .bashrc
    '''
    c = Configuration()

    # gen the directory
    if not os.path.exists(c.conf_dir_name):
        os.makedirs(c.conf_dir_name)
    # gen the conf file
    if not os.path.exists(c.conf_file_name):
        gen_default_configuration()
    # gen the projects directory
    if not os.path.exists(c.projects_dir_name):
        os.makedirs(c.projects_dir_name)

    # cp gvenv into the new directory
    shutil.copy(p_name, c.conf_dir_name)
    shutil.copy('configuration.py', c.conf_dir_name)
    shutil.copy('source.sh', c.conf_dir_name)


def new_project(project_name, conf):
    '''
    create the virtual environment for the project in the position defined in
    the configuration file
    '''

    # get the default directory for virtual environments
    dir_gvenv = conf.projects_dir_name
    dir_gvenv_project = path.join(dir_gvenv, project_name)

    env = EnvBuilder()

    # create new directory of the virtual environment
    print(('Generating new environment in {0}'.format(dir_gvenv)))
    env.create(dir_gvenv_project)
    print('done.')


def activate_project(project_name, conf):
    '''
    activate the project venv
    '''
    b = 'bin'
    activate = 'activate'
    venv_path = path.join(conf.projects_dir_name, project_name, b, activate)
    #cmd_source = path.join(conf.conf_dir_name, 'source.sh')

    # TODO: substitute it with an automatic "source"
    print(('For activate the venv, launch from the shell the command:\n\n' +
          'source {0}'.format(venv_path)))


def show_projects(conf):
    '''
    show all the virtual environments stored in the gvenv directory
    '''
    dir_projects = conf.projects_dir_name
    projects = os.listdir(dir_projects)

    # sort the projects
    projects = sorted(projects)

    i = 1
    for project in projects:
        print(("{0}\t {1}".format(i, project)))
        i += 1


def show_help():
    print(('List of commands : \n' +
    'new\n' +
    '--help\n' +
    'activate\n' +
    'defaultconf\n' +
    'show\n' +
    'install'))


def gen_default_configuration():
    '''
    generate new default configuration and store it in the main folder of gvenv
    '''
    c = Configuration()
    d_conf = c.generate_default_configuration()

    # save d_conf
    conf_file = open(c.conf_file_name, 'w')
    conf_file.write(d_conf)
    conf_file.close()

    pass


def main(args):
    '''
    parse the user input that are :
        --help
        show
        defaultconf [installation path of gvenv]
        new [project name]
        activate [project name]
    '''
    # get inputs
    p_name = args[0]
    if len(args) == 2:
        usage = args[1]
    elif len(args) == 3:
        usage = args[1]
        value = args[2]
    else:
        show_help()
        return 0

    # check if the program is installed, if not suggest to install using
    # gvenv install
    if not check_installation() and usage != 'install':
        print(('''{0} is not installed correctly.\
Install it typing {0} install'''.format(p_name)))
        return 0

    # check inputs
    if usage not in USAGES:
        # show help and close the program
        print(('{0} is not a possible input'.format(usage)))
        show_help()
        return 0

    # get configuration
    c = Configuration()
    #dconf = c.load_configuration()

    if usage == 'new':
        new_project(value, c)
    elif usage == 'activate':
        activate_project(value, c)
    elif usage == 'defaultconf':
        gen_default_configuration()
    elif usage == 'show':
        show_projects(c)
    elif usage == 'install':
        install(p_name)
    elif usage == '--help':
        show_help()
    else:
        print('Some error in the input')
        show_help()

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
