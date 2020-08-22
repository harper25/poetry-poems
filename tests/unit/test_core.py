""" Test Core Functions """

import pytest  # noqa: F401
import os
from tempfile import mkdtemp

from pipenv_pipes.core import (
    find_environments,
    find_binary,
    get_binary_version,
    delete_directory,
)


class TestFindEnvironments():

    def test_find_environments(self, mock_env_home):
        pipenv_home, mock_projects_dir = mock_env_home
        # Add a non env to mock projects ensure it's not picked up
        os.makedirs(os.path.join(pipenv_home, 'notanenv'))
        environments = find_environments(pipenv_home)
        assert len(environments) == 2
        assert 'proj1' in [e.project_name for e in environments]

    def test_find_environments_empty(self, temp_folder):
        """ Environment could be empty """
        environments = find_environments(temp_folder)
        assert len(environments) == 0

    def test_delete_directory(self):
        """ Ensure delete directory  """
        temp_folder = mkdtemp()
        assert os.path.isdir(temp_folder)
        assert delete_directory(temp_folder)
        assert not os.path.exists(temp_folder)

    def test_find_environments_does_not_exit(self):
        """ Invalid Folder. CLI Entry should catch, core func should fail """
        with pytest.raises(IOError):
            find_environments('/fakedir/')

    def test_find_binary(self, mock_env_home, temp_folder):
        pipenv_home, mock_projects_dir = mock_env_home
        envname = os.listdir(pipenv_home)[0]
        envpath = os.path.join(pipenv_home, envname)
        binpath = find_binary(envpath)
        assert 'python' in binpath
        assert envpath in binpath
        with pytest.raises(EnvironmentError):
            find_binary(temp_folder)

    def test_get_python_version(self, mock_env_home, temp_folder):
        pipenv_home, mock_projects_dir = mock_env_home
        envname = os.listdir(pipenv_home)[0]
        envpath = os.path.join(pipenv_home, envname)
        assert 'Python' in get_binary_version(envpath)
