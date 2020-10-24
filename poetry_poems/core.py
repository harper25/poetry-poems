import os

from poetry_poems.poetry import call_poetry_env, call_python_version
from poetry_poems.utils import collapse_path


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
            virtualenv_output, code = call_poetry_env(self.project_path)
            if code != 0 or not virtualenv_output:
                raise (
                    EnvironmentError(
                        "No virtual environment associated with project: "
                        f"{collapse_path(self.project_path)}"
                    )
                )
            self._envpath = virtualenv_output.split()[0]
        return self._envpath

    @property
    def binpath(self):
        """ Finds the python binary in a given environment path """
        if self._binpath is None:
            env_ls = os.listdir(self.envpath)
            if "bin" in env_ls:
                binpath = os.path.join(self.envpath, "bin", "python")
            elif "Scripts" in env_ls:
                binpath = os.path.join(self.envpath, "Scripts", "python.exe")
            else:
                raise EnvironmentError(
                    f"could not find python binary path: {collapse_path(self.envpath)}"
                )
            if os.path.exists(binpath):
                self._binpath = binpath
            else:
                raise EnvironmentError(f"could not find python binary: {collapse_path(binpath)}")

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
