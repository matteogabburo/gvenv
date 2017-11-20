#!/usr/bin/env python3.5
import sys
from pathlib import Path
import os.path as path

CONF_FILE_NAME = 'gvenv.conf'
FOLDER_NAME = '.gvenv'
FOLDER_PROJECT_NAME = 'projects'
ROW_SEPARATOR = '\n'
KEY_VALUE_SEPARATOR = '='
KEYS = ('path_dir_envs', 'path_dir_venv_projects')


class Configuration:
    '''
    load the configuration from the conf file (path defined in CONF_FILE_NAME)

    example of configuration file where key,value separator is '=' and row
    separator is '\n':

        key1=value1
        key2=value2
        ...
        keyN=valueN
    '''
    def __init__(self):
        '''
        constructor of the class configuration, declare all the variables of
        the configuration file
        '''
        home = Path.home()
        self.conf_dir_name = path.join(home, FOLDER_NAME)
        self.conf_file_name = path.join(home, FOLDER_NAME, CONF_FILE_NAME)
        self.projects_dir_name = path.join(home, FOLDER_NAME,
                                            FOLDER_PROJECT_NAME)
        self.conf_keys = KEYS
        #self.dconf = property(self.load_configuration)

    def load_configuration(self):
        '''
        load the configuration from the conf file, if the file is corrupted or
        not exists, launch an exception and close the program
        '''
        # check if the file exist
        conf_file_path = Path(self.conf_file_name)
        if conf_file_path.is_file():
            # get the text from the configuration file
            print('Found an existent configruation file, importing... ')
            conf_file = open(self.conf_file_name, 'r')
            conf_text = conf_file.read()
            conf_file.close()
            print('Done.')

            #split conf in rows, and for each row extract the key,value pair
            dconf = {}
            rows = conf_text.split(ROW_SEPARATOR)
            for row in rows:
                values = row.split(KEY_VALUE_SEPARATOR)
                key = values[0]
                value = values[1]
                if key in KEYS:
                    dconf[key] = value
        else:
            print('WARNING: Didn\'t found any existend configuration.')
            print('Generate a new configuration typing "gvenv defaultconf"')
            sys.exit()

        return dconf

    def generate_default_configuration(self):
        '''
        generate a default configuration file in the main directory of gvenv
        '''
        # make default conf
        home = Path.home()
        new_path_dir = path.join(home, self.conf_dir_name)
        new_path_dir_project = path.join(new_path_dir, self.projects_dir_name)

        path_dir = KEY_VALUE_SEPARATOR.join(('path_dir_envs', new_path_dir))
        path_dir_projects = KEY_VALUE_SEPARATOR.join(('path_dir_venv_projects',
                                                     new_path_dir_project))

        default_conf = ROW_SEPARATOR.join((path_dir,
                                          path_dir_projects))

        return default_conf
