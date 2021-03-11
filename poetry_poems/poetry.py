import os
import sys
from subprocess import PIPE, Popen


def PipedPopen(cmds, **kwargs):
    """ Helper Piped Process for drier code"""
    timeout = kwargs.pop("timeout", None)
    env = kwargs.pop("env", dict(os.environ))

    # For Windows we must explicitly state that a command should be run as a
    # shell command
    run_as_shell = sys.platform == "win32"
    proc = Popen(cmds, stdout=PIPE, stderr=PIPE, env=env, shell=run_as_shell, **kwargs)
    out, err = proc.communicate(timeout=timeout)
    output = out.decode().strip() or err.decode().strip()
    code = proc.returncode
    return output.strip(), code


def call_poetry_shell(cwd, envname="poetry-shell", timeout=None):
    """ Calls ``poetry shell``` from a given envname """
    environ = dict(os.environ)
    environ["PROMPT"] = f"({envname}){os.getenv('PROMPT', '')}"

    is_test = "PYTEST_CURRENT_TEST" in os.environ
    stdout = PIPE if is_test else sys.stdout
    stderr = PIPE if is_test else sys.stderr

    # For Windows we must explicitly state that a command should be run as a
    # shell command
    run_as_shell = sys.platform == "win32"
    proc = Popen(
        ["poetry", "shell"],
        cwd=cwd,
        shell=run_as_shell,
        stdout=stdout,
        stderr=stderr,
        env=environ,
    )
    out, err = proc.communicate(timeout=timeout)
    output = out or err
    code = proc.returncode
    return output, code, proc


def call_python_version(pybinpath):
    binpath = os.path.dirname(pybinpath)
    pybinpath = os.path.join(binpath, "python")
    output, code = PipedPopen(cmds=[pybinpath, "--version"])
    return output, code


def call_poetry_env(project_dir):
    """ Calls ``poetry env`` from a given project directory """
    output, code = PipedPopen(cmds=["poetry", "env", "list", "--full-path"], cwd=project_dir)
    return output, code


class PoetryConfig:
    def __init__(self):
        self.errors = []
        self.poetry_home = ""
        self.virtualenv_in_project = ""
        self.call_poetry_virtualenvs_path()

    def call_poetry_virtualenvs_path(self):
        output, code = PipedPopen(cmds=["poetry", "config", "virtualenvs.path"])
        if code != 0:
            self.errors.append(output)
        else:
            self.poetry_home = output

    def call_poetry_virtualenv_in_project(self):
        output, code = PipedPopen(cmds=["poetry", "config", "virtualenvs.in-project"])
        if code != 0:
            self.errors.append(output)
        else:
            self.virtualenv_in_project = output

    def validate(self):
        if self.errors:
            error = "\n".join(self.errors)
            error_msg = f"Poetry config errors:\n {error}"
            return error_msg
        return
