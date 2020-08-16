
import os
import shutil
import time
from collections import namedtuple

from .pipenv import call_python_version
from .utils import (
    get_project_name,
    get_project_dir_filepath,
)

Environment = namedtuple('Environment', [
    'envpath',
    'envname',
    'project_name',
    'binpath',
    ])


def find_poetry_projects(poems_file):
    print()
    print(poems_file)
    mode = 'r' if os.path.exists(poems_file) else 'a+'

    with open(poems_file, mode) as f:
        project_folders = f.read()
    project_folders = project_folders.splitlines()
    return project_folders


def add_new_poem(new_poem_path, project_names, poems_file):
    if new_poem_path in project_names:
        return 'Project already saved in poems!'

    with open(poems_file, 'a') as f:
        f.write(f'{new_poem_path}\n')


def find_environments(poetry_home):
    """
    Returns Environment NamedTuple created from list of folders found in the
    Poetry Environment location
    """
    environments = []
    for folder_name in sorted(os.listdir(poetry_home)):
        envpath = os.path.join(poetry_home, folder_name)
        project_name = get_project_name(folder_name)
        if not project_name:
            continue

        binpath = find_binary(envpath)
        environment = Environment(project_name=project_name,
                                  envpath=envpath,
                                  envname=folder_name,
                                  binpath=binpath,
                                  )
        environments.append(environment)
    return environments


def find_binary(envpath):
    """ Finds the python binary in a given environment path """
    env_ls = os.listdir(envpath)
    if 'bin' in env_ls:
        binpath = os.path.join(envpath, 'bin', 'python')
    elif 'Scripts' in env_ls:
        binpath = os.path.join(envpath, 'Scripts', 'python.exe')
    else:
        raise EnvironmentError(
            'could not find python binary path: {}'.format(envpath))
    if os.path.exists(binpath):
        return binpath
    else:
        raise EnvironmentError(
            'could not find python binary: {}'.format(envpath))


def get_binary_version(envpath):
    """ Returns a string indicating the Python version (Python 3.5.6) """
    pybinpath = find_binary(envpath)
    output, code = call_python_version(pybinpath)
    if not code:
        return output
    else:
        raise EnvironmentError(
            'could not get binary version: {}'.format(output))


def delete_directory(envpath):
    """ Deletes the enviroment by its path """
    attempt = 0
    while attempt < 5:
        try:
            shutil.rmtree(envpath)
        except (FileNotFoundError, OSError):
            pass
        if not os.path.exists(envpath):
            return True
        attempt += 1
        time.sleep(0.25)


###############################
# Project Dir File (.project) #
###############################


def read_project_dir_file(envpath):
    project_file = get_project_dir_filepath(envpath)
    try:
        with open(project_file) as fp:
            return fp.read().strip()
    except IOError:
        return


def write_project_dir_project_file(envpath, project_dir):
    project_file = get_project_dir_filepath(envpath)
    with open(project_file, 'w') as fp:
        return fp.write(project_dir)
