""" Test Core Functions """

import os

import pytest  # noqa: F401

from poetry_poems.core import (
    add_new_poem,
    delete_poem_from_poems_file,
    generate_environments,
    read_poetry_projects,
)


def test_add_new_poem_already_saved(project_paths, poems_file):
    new_poem_path = project_paths[0]
    result = add_new_poem(new_poem_path, project_paths, poems_file)
    assert result == "Project already saved in poems!"


def test_add_new_poem_invalid_paths(project_paths, poems_file):
    new_poem_path = f"{project_paths}/new_nested_project"
    result = add_new_poem(new_poem_path, project_paths, poems_file)
    assert "The new path belongs to already saved project" in result


def test_add_new_poem(project_paths, empty_poems_file):
    new_poem_path = "/my_repos/new_project"
    result = add_new_poem(new_poem_path, project_paths, empty_poems_file)
    assert result is None

    with open(empty_poems_file, "r") as f:
        saved_projects = f.read()
        saved_projects = saved_projects.splitlines()
    assert saved_projects == [new_poem_path]


def test_read_poetry_projects(project_paths, poems_file):
    assert read_poetry_projects(poems_file) == project_paths


def test_delete_poem_from_poems_file(project_paths, poems_file):
    delete_poem_from_poems_file(project_paths[0], list(project_paths), poems_file)

    with open(poems_file, "r") as f:
        saved_projects = f.read()
        saved_projects = saved_projects.splitlines()
    assert saved_projects == project_paths[1:]


def test_generate_environments(project_paths, simple_environments):
    environments = generate_environments(project_paths)
    assert environments == simple_environments


def test_environment_no_envpath(simple_environments):
    env = simple_environments[0]
    with pytest.raises(EnvironmentError) as e:
        env.envpath
    assert "No virtual environment associated with project" in str(e)


def test_environment_no_binpath(simple_environments):
    env = simple_environments[0]
    fake_envpath = os.path.join(env.project_path, "envpath")
    os.makedirs(fake_envpath)
    env._envpath = fake_envpath
    with pytest.raises(EnvironmentError) as e:
        env.binpath
    assert "could not find python binary path" in str(e)


def test_environment_binpath(simple_environments):
    env = simple_environments[0]
    fake_envpath = os.path.join(env.project_path, "envpath")
    fake_binpath = os.path.join(fake_envpath, "bin/python")
    os.makedirs(fake_binpath)
    env._envpath = fake_envpath
    assert env.binpath == fake_binpath


@pytest.mark.parametrize("venv_path", ["bin", "Scripts"])
def test_environment_python_binary_missing(venv_path, simple_environments):
    env = simple_environments[0]
    fake_envpath = os.path.join(env.project_path, "envpath")
    invalid_fake_binpath = os.path.join(fake_envpath, venv_path)
    os.makedirs(invalid_fake_binpath)
    env._envpath = fake_envpath
    with pytest.raises(EnvironmentError) as e:
        env.binpath
    assert "could not find python binary" in str(e)


def test_environment_python_binversion_error(simple_environments):
    env = simple_environments[0]
    fake_envpath = os.path.join(env.project_path, "envpath")
    intermediate_path = os.path.join(fake_envpath, "bin")
    os.makedirs(intermediate_path)
    fake_binpath = os.path.join(intermediate_path, "python")
    open(fake_binpath, "w").close()
    env._envpath = fake_envpath
    env._binpath = fake_binpath
    with pytest.raises(EnvironmentError) as e:
        env.binversion
    assert "Permission denied" in str(e)


def test_environment_python_binversion(simple_environments, venv_fresh):
    env = simple_environments[0]
    fake_envpath = venv_fresh
    env._envpath = fake_envpath
    env._binpath = os.path.join(fake_envpath, "bin/python")
    assert "Python" in env.binversion
