import os
import tempfile
from contextlib import contextmanager
from subprocess import PIPE, Popen
from tempfile import TemporaryDirectory

import pytest
from click.testing import CliRunner

from poetry_poems.core import Environment
from poetry_poems.environment import EnvVars

HERE = os.path.dirname(__file__)


def touch(filename):
    try:
        os.utime(filename, None)
    except OSError:
        open(filename, "a").close()


@pytest.fixture
def env_vars():
    return EnvVars()


@pytest.fixture(scope="session")
def venv_fresh():
    with TemporaryDirectory() as folder:
        venv_cmd = "virtualenv --no-pip --no-wheel --no-setuptools"
        cmd = f"{venv_cmd} {folder}"
        proc = Popen(cmd.split(" "), stderr=PIPE, stdout=PIPE)
        out, err = proc.communicate()
        if err:
            raise Exception(err)
        yield folder


@pytest.fixture
def win_tempdir(env_vars):
    # Default %TEMP% returns windows short path (C:\\Users\\GTALAR~1\\AppData)
    # The`~1`` breaks --venv hash resolution, so we must build path manually
    # On other systems this will be none, so default env will be used
    if not env_vars.IS_WINDOWS:
        return None
    path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Temp")
    assert "~" not in path
    assert os.path.exists(path)
    return path


@pytest.fixture(scope="function")
def temp_folder():
    """ A folderpath with for an empty folder """
    with TemporaryDirectory() as path:
        yield path


@pytest.fixture(scope="session")
def session_scoped_temp_folder():
    """ A folderpath with for an empty folder """
    with TemporaryDirectory() as path:
        yield path


@pytest.fixture(scope="session")
def project_names():
    return ["project_1", "project_2", "project_with_virtualenv"]


@pytest.fixture(scope="function")
def project_paths(project_names, temp_folder, project_with_virtualenv):
    paths = []
    for name in project_names[:2]:
        project_path = os.path.join(temp_folder, name)
        paths.append(project_path)
        os.mkdir(project_path)
    paths.append(project_with_virtualenv)
    return paths


@pytest.fixture(scope="function")
def poems_file(temp_folder, project_paths):
    temp_file = tempfile.NamedTemporaryFile(mode="w", delete=False, dir=temp_folder)

    with temp_file as f:
        f.write("\n".join(project_paths) + "\n")

    return temp_file.name


@pytest.fixture(scope="function")
def empty_poems_file(temp_folder):
    temp_file = tempfile.NamedTemporaryFile(mode="w", delete=False, dir=temp_folder)
    return temp_file.name


@pytest.fixture(scope="function")
def save_to_poems_file(poems_file):
    def handler(poems_file=poems_file, environment=None, project_path=None):
        project_path = project_path or environment.project_path

        with poems_file(mode="a") as f:
            f.write(f"{project_path}\n")


@pytest.fixture(scope="function")
def simple_environments(project_names, project_paths):
    environments = []
    for name, path in zip(project_names, project_paths):
        environments.append(Environment(project_path=path, project_name=name, envname=name))
    return environments


@pytest.fixture(scope="session")
def project_with_virtualenv(session_scoped_temp_folder):
    project_path = os.path.join(session_scoped_temp_folder, "project_with_virtualenv")

    poetry_new_cmd = "poetry new project_with_virtualenv"
    proc = Popen(
        poetry_new_cmd.split(" "), stderr=PIPE, stdout=PIPE, cwd=session_scoped_temp_folder
    )
    out, err = proc.communicate()
    if err:
        raise Exception(err)

    new_venv_path = os.path.join(project_path, ".venv")

    venv_cmd = f"virtualenv --no-pip --no-wheel --no-setuptools {new_venv_path}"
    proc = Popen(venv_cmd.split(" "), stderr=PIPE, stdout=PIPE)
    out, err = proc.communicate()
    if err:
        raise Exception(err)

    poetry_config_cmd = "poetry config --local virtualenvs.in-project true"
    proc = Popen(poetry_config_cmd.split(" "), stderr=PIPE, stdout=PIPE, cwd=project_path)
    out, err = proc.communicate()
    if err:
        raise Exception(err)

    yield project_path


@contextmanager
def _TempEnviron(**env):
    old_environ = dict(os.environ)
    os.environ.pop("PIPENV_ACTIVE", None)
    os.environ.pop("POETRY_ACTIVE", None)
    os.environ.pop("VENV", None)
    os.environ.pop("VIRTUAL_ENV", None)
    os.environ.update(env)
    yield
    os.environ.clear()
    os.environ.update(old_environ)


@pytest.fixture
def TempEnviron():
    """
    >>> with TempEnviron(WORKON_HOME=temp_fake_venvs_home):
    >>>    # do something
    """
    return _TempEnviron


@pytest.fixture
def mock_projects_dir(project_names, win_tempdir):
    """ A folderpath with 2 sample project folders """
    with TemporaryDirectory(prefix="projects", dir=win_tempdir) as projects_dir:
        for project_name in project_names:
            os.makedirs(os.path.join(projects_dir, project_name))
        yield projects_dir


@pytest.fixture
def runner(TempEnviron):
    with TempEnviron():
        runner = CliRunner()
        yield runner


@pytest.fixture(name="environments")
def fake_environments():
    """ Used by unit.test_pick parametrics tests """
    from poetry_poems.core import Environment

    return [
        Environment(project_path="/", project_name="proj1", envname="proj1-1C_-wqgW"),
        Environment(project_path="/", project_name="proj2", envname="proj2-12345678"),
        Environment(project_path="/", project_name="abc-o", envname="abc-o-12345678"),
        Environment(project_path="/", project_name="notpipenv", envname="notpipenv"),
    ]
