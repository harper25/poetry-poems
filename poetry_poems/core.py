import os
import re

from poetry_poems.poetry import call_poetry_env, call_python_version
from poetry_poems.utils import collapse_path

ANSI_ESCAPE_PATTERN = re.compile(r"(?:\x1B[@-_]|[\x80-\x9F])[0-?]*[ -/]*[@-~]")


class Environment:
    def __init__(self, project_name, project_path, envname):
        self.project_name = project_name
        self.project_path = project_path
        self.envname = envname
        self._envpath = None
        self._binpath = None
        self._binversion = None

    def __str__(self):
        return (
            f"Environment(project_name={self.project_name}, "
            f"project_path={self.project_path}, "
            f"envname={self.envname}, "
            f"envpath={self._envpath}, "
            f"binpath={self._binpath}, "
            f"binversion={self._binversion})"
        )

    def __eq__(self, other):
        return str(self) == str(other)

    # For .venv in project: poetry config --local virtualenvs.in-project true
    @property
    def envpath(self):
        if self._envpath is None:
            if not os.path.exists(self.project_path):
                self._envpath = "Project directory does not exist!"
            else:
                virtualenv_output, code = call_poetry_env(self.project_path)
                if code != 0 or not virtualenv_output:
                    self._envpath = (
                        "No virtual environment associated with project: "
                        f"{collapse_path(self.project_path)}"
                    )
                else:
                    envpath = ANSI_ESCAPE_PATTERN.sub("", virtualenv_output)
                    self._envpath = envpath.split()[0]
        if not os.path.exists(self._envpath):
            raise EnvironmentError(self._envpath)
        return self._envpath

    @property
    def binpath(self):
        """ Finds the python binary in a given environment path """
        if self._binpath is None:
            general_error_msg = (
                f"Could not find python binary path: {collapse_path(self.envpath)}"
            )
            if not os.path.exists(self.envpath):
                self._binpath = general_error_msg
            elif "bin" in os.listdir(self.envpath) and os.path.exists(
                os.path.join(self.envpath, "bin", "python")
            ):
                self._binpath = os.path.join(self.envpath, "bin", "python")
            elif "Scripts" in os.listdir(self.envpath) and os.path.exists(
                os.path.join(self.envpath, "Scripts", "python.exe")
            ):
                self._binpath = os.path.join(self.envpath, "Scripts", "python.exe")
            else:
                self._binpath = general_error_msg
        if not os.path.exists(self._binpath):
            raise EnvironmentError(self._binpath)
        return self._binpath

    @property
    def binversion(self):
        """ Returns a string indicating the Python version (Python 3.5.6) """
        if self._binversion is None:
            output, code = call_python_version(self.binpath)
            if not code:
                self._binversion = output
            else:
                raise EnvironmentError(f"could not get binary version: {output}")
        return self._binversion


def read_poetry_projects(poems_file):
    mode = "r" if os.path.exists(poems_file) else "a+"
    with open(poems_file, mode) as f:
        project_paths = f.read()
    project_paths = project_paths.splitlines()
    return project_paths


def add_new_poem(new_poem_path, project_paths, poems_file):
    if new_poem_path in project_paths:
        return "Project already saved in poems!"

    with open(poems_file, "a") as f:
        f.write(f"{new_poem_path}\n")


# For .venv in project: poetry config --local virtualenvs.in-project true
def generate_environments(project_paths):
    """
    Returns Environments created from list of folders with poems.
    """
    environments = []
    for project_path in project_paths:
        project_name = os.path.basename(project_path)

        environment = Environment(
            project_path=project_path, project_name=project_name, envname=project_name
        )
        environments.append(environment)
    return environments


def delete_poem_from_poems_file(project_path_to_delete, project_paths, poems_file):
    """ Delete the poem from paths saved in poems file """
    project_paths.remove(project_path_to_delete)

    with open(poems_file, "w") as f:
        f.write("\n".join(project_paths) + "\n")
