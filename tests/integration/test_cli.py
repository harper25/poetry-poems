#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Tests for `poetry-poems` cli."""
import os

import pytest  # noqa: F401
from poetry_poems.cli import poems


def test_cli_help(runner):
    help_result = runner.invoke(poems, args=['--help'])
    assert help_result.exit_code == 0
    assert 'show this message and exit' in help_result.output.lower()


def test_cli_version(runner):
    from poetry_poems import __version__
    result = runner.invoke(poems, args=['--version'], catch_exceptions=False)
    assert result.exit_code == 0
    assert __version__ in result.output


def test_cli_from_shell():
    import subprocess
    result = subprocess.check_output(['poems', '--help']).decode()
    assert 'show this message and exit' in result.lower()


# @pytest.mark.curses
def test_cli_no_args(runner, poems_file):
    result = runner.invoke(poems, args=['--poems_file', poems_file])
    assert result.exit_code == 1
    assert 'query": ""' in result.output
    assert 'envs": 3' in result.output


# @pytest.mark.curses
def test_cli_no_args_verbose(runner, poems_file):
    result = runner.invoke(
        poems, ['--poems_file', poems_file, '--verbose'], catch_exceptions=False)
    assert result.exit_code == 1
    assert 'POETRY_HOME' in result.output


# @pytest.mark.curses
def test_many_match(runner, poems_file):
    result = runner.invoke(poems, args=['--poems_file', poems_file, 'project'])
    assert result.exit_code == 1
    assert 'query": "project' in result.output
    assert 'envs": 3' in result.output


def test_cli_list(runner, poems_file, project_names):
    result = runner.invoke(
        poems, args=['--poems_file', poems_file, '--list'], catch_exceptions=False)
    assert result.exit_code == 0
    assert project_names[0] in result.output
    assert project_names[1] in result.output


def test_cli_list_verbose(runner, poems_file):
    result = runner.invoke(
        poems, args=['--poems_file', poems_file, '--list', '--verbose'], catch_exceptions=False)
    assert result.exit_code == 0
    assert 'POETRY_HOME' in result.output
    assert '-- Not configured --' in result.output  # virtualenv is missing


def test_cli_delete_env(runner, poems_file, project_names):
    result = runner.invoke(
        poems, args=['--poems_file', poems_file, project_names[0], '--delete'], catch_exceptions=False,
        input='y')
    assert result.exit_code == 0
    assert 'deleted' in result.output

    with open(poems_file, 'r') as f:
        project_paths = f.read()

    assert project_names[0] not in project_paths
    assert project_names[1] in project_paths


def test_cli_delete_env_abort(runner, poems_file, project_names):
    result = runner.invoke(
        poems, args=['--poems_file', poems_file, project_names[0], '--delete'], catch_exceptions=False,
        input='n')
    assert result.exit_code == 0
    assert 'not deleted' in result.output

    with open(poems_file, 'r') as f:
        project_paths = f.read()

    assert project_names[0] in project_paths
    assert project_names[1] in project_paths


def test_no_match(runner, poems_file):
    result = runner.invoke(
        poems, args=['--poems_file', poems_file, 'projxxx'], catch_exceptions=False)
    assert result.exit_code == 0
    assert 'no matches' in result.output.lower()


def test_no_environments(runner, temp_folder):
    fake_poems_file = os.path.join(temp_folder, 'fake_poems_file')
    open(fake_poems_file, 'w').close()
    result = runner.invoke(poems, args=['--poems_file', fake_poems_file])
    assert result.exception
    assert 'no poems found in poems file:' in result.output.lower()


def test_add_new_environment_path_does_not_exist(runner, poems_file):
    result = runner.invoke(
        poems, args=['--poems_file', poems_file, '--add', 'fakepath'], catch_exceptions=False)
    assert result.exit_code == 1
    assert "Path 'fakepath' does not exist" in result.output


def test_add_new_environment_no_virtualenv(runner, poems_file, temp_folder):
    new_project = os.path.join(temp_folder, 'new_project')
    os.makedirs(new_project)
    result = runner.invoke(
        poems, args=['--poems_file', poems_file, '--add', new_project], catch_exceptions=False)
    assert result.exit_code == 1
    assert "No virtualenv associated with the project" in result.output


def test_one_match_do_shell(runner, poems_file, project_names, project_with_virtualenv):
    result = runner.invoke(
        poems, args=['--poems_file', poems_file, 'project_with_virtualenv'], input='exit', catch_exceptions=False)
    assert result.exit_code == 0
    assert 'Terminating Poems Shell' in result.output


def test_completions(runner, poems_file, project_names):
    result = runner.invoke(
        poems, args=['--poems_file', poems_file, '--_completion'], catch_exceptions=False)
    assert result.exit_code == 0
    assert project_names[0] in result.output
    assert project_names[1] in result.output


@pytest.mark.parametrize("env_var, error_msg", [
    ('POETRY_ACTIVE', 'Poetry Shell is already active'),
    ('PIPENV_ACTIVE', 'Pipenv Shell is already active'),
    ('VENV', 'Virtual environment is already active'),
    ('VIRTUAL_ENV', 'Virtual environment is already active'),
])
def test_env_vars_errors(env_var, error_msg, runner, poems_file):
    env = {env_var: '1'}
    result = runner.invoke(poems, args=['--poems_file', poems_file], env=env)
    assert result.exception
    assert error_msg in result.output
