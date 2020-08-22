
import os
import shutil
import time
from collections import namedtuple

from .pipenv import call_python_version, call_poetry_env
from .utils import (
    get_project_name,
)

Environment = namedtuple('Environment', [
    'project_path',
    'envpath',
    'envname',
    'project_name',
    'binpath',
    ])  # remove project_name?


def find_poetry_projects(poems_file):
    mode = 'r' if os.path.exists(poems_file) else 'a+'
    with open(poems_file, mode) as f:
        project_paths = f.read()
    project_paths = project_paths.splitlines()
    return project_paths


def add_new_poem(new_poem_path, project_names, poems_file):
    if new_poem_path in project_names:
        return 'Project already saved in poems!'

    with open(poems_file, 'a') as f:
        f.write(f'{new_poem_path}\n')


def find_environments_in_poetry_home(poetry_home):
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
        environment = Environment(
                                  project_path='',
                                  project_name=project_name,
                                  envpath=envpath,
                                  envname=folder_name,
                                  binpath=binpath,
                                  )
        environments.append(environment)
    return environments


# For .venv in project: poetry config --local virtualenvs.in-project true
def find_environments(project_paths):
    """
    Returns Environment NamedTuple created from list of folders found in the
    Poetry Environment location
    """
    environments = []
    for project_path in project_paths:
        # project_name = get_project_name(envpath)
        project_name = os.path.split(project_path)
        if not project_name or len(project_name) != 2:
            continue

        project_name = project_name[1]
        virtualenv_output, code = call_poetry_env(project_path)
        # raise EnvironmentError
        print(virtualenv_output)

        # For .venv in project: poetry config --local virtualenvs.in-project true
        virtualenv_path = virtualenv_output.split()[0]

        binpath = find_binary(virtualenv_path)
        environment = Environment(
                                  project_path=project_path,
                                  project_name=project_name,
                                  envpath=virtualenv_path,
                                  envname=project_name,
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
