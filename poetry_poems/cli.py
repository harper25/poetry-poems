# -*- coding: utf-8 -*-

""" Poems: Poetry Shell Switcher """

import sys
import click
import os

from . import __version__
from .environment import EnvVars
from .picker import Picker
from .utils import get_query_matches, collapse_path
from .poetry import (
    call_poetry_shell,
    PoetryConfig,
    call_poetry_env
)
from .core import (
    find_environments,
    find_environments_in_poetry_home,
    get_binary_version,
    delete_directory,
    read_poetry_projects,
    add_new_poem
)


@click.command()
@click.argument('envname', default='', required=False)
@click.option(
    '--list', 'list_',
    is_flag=True,
    help='List Poetry Projects')
@click.option('--delete', '-d', 'delete',
              is_flag=True,
              help='Deletes the target Enviroment')
@click.option('--verbose', '-v', is_flag=True, help='Verbose')
@click.option('--version', is_flag=True, help='Show Version')
@click.option(
    '-p',
    '--poems_file',
    type=click.Path(exists=False),
    default=lambda: f"{os.environ.get('HOME', '')}/.poetry-poems",
    help='A path to the file listing all poems.',
)
@click.option('--add', '-a', 'new_poem_path',
              type=click.Path(exists=False),
              default="",
              help='A path to a new poem.')
@click.pass_context
def poems(ctx, envname, list_, verbose, version, delete, poems_file, new_poem_path):
    """

    Poems - Poetry Environment Switcher

    Go To Project:\n
        >>> poems envname

    Delete an Environment:\n
        >>> poems envname --delete

    See all Poetry Environments:\n
        >>> poems --list
        >>> poems --list --verbose

    """
    if version:
        click.echo(__version__)
        return

    poetry_config = PoetryConfig()
    env_vars = EnvVars()

    if env_vars.HAS_CURSES:
        import curses # noqa flake8

    ensure_poetry_config_is_ok(poetry_config)
    ensure_env_vars_are_ok(env_vars)

    project_paths = read_poetry_projects(poems_file)

    environments = find_environments(project_paths)
    # environments = find_environments_in_poetry_home(poetry_config.poetry_home)
    if not environments:
        click.echo(
            f'No poetry environments (poems) found in poems file: {poems_file}\n'
            'Please, add a new poem with a command: poems --add --path <path-to-your-poem>')
        sys.exit(1)

    if verbose:
        click.echo('\nPOETRY_HOME: {}\n'.format(poetry_config.poetry_home))

    if list_:
        print_project_list(environments=environments, verbose=verbose)
        sys.exit(0)

    if new_poem_path:
        new_poem_path = parse_new_poem_path(new_poem_path)
        ensure_path_exists(new_poem_path)
        ensure_project_dir_has_env(new_poem_path)
        error_msg = add_new_poem(new_poem_path, project_paths, poems_file)
        if error_msg:
            click.echo(click.style(error_msg, fg='yellow'))
            sys.exit(1)
        sys.exit(0)

    matches = get_query_matches(environments, envname)
    environment = ensure_one_match(envname, matches, environments)

    if delete:
        if not click.confirm(
            "Are you sure you want to delete '{}'".format(environment.envpath),
            default=False
        ):
            click.echo('Environment not deleted')
            sys.exit(0)
        if delete_directory(environment.envpath):
            msg = "Environment '{}' deleted".format(environment.envname)
            click.echo(click.style(msg, fg='yellow'))
        else:
            msg = 'Could not delete enviroment {}'.format(environment.envpath)
            click.echo(click.style(msg, fg='red'))
        sys.exit(0)

    else:
        launch_env(environment)


def launch_env(environment):
    """ Launch Poetry Shell """

    project_dir = environment.project_path
    msg_dir = click.style(
        "Project directory: '{}'".format(project_dir), fg='yellow')
    msg_env = click.style(
        "Environment: '{}'".format(environment.envpath), fg='yellow')
    click.echo(msg_dir)
    click.echo(msg_env)

    call_poetry_shell(cwd=project_dir, envname=environment.envname)

    msg = 'Terminating Poems Shell...'
    click.echo(click.style(msg, fg='red'))
    sys.exit(0)


def do_pick(environments, query=None):
    picker = Picker(environments, query=query, debug_mode=False)
    selected = picker.start()
    return selected


def print_project_list(environments, verbose):
    """ Prints Environments List """

    for index, environment in enumerate(environments):
        project_dir = environment.project_path
        has_project_dir = bool(project_dir)
        name = click.style(environment.envname, fg='yellow')
        envpath = click.style(environment.envpath, fg='blue')
        binversion = get_binary_version(environment.envpath)
        index = click.style(str(index), fg='red')

        entry = ' {}: {}'.format(index, name)
        if has_project_dir:
            entry += ' *'
            project_dir = click.style(project_dir, fg='blue')
        else:
            project_dir = click.style('[ NOT SET ]', fg='red')

        entry = name if not has_project_dir else name + ' *'
        if not verbose:
            click.echo(entry)
        else:
            click.echo(
                '{entry}\n'
                '    Environment: \t {envpath}\n'
                '    Binary: \t\t {binversion}\n'
                '    Project Dir: \t {project_dir}\n'
                .format(
                    entry=entry,
                    envpath=collapse_path(envpath),
                    project_dir=collapse_path(project_dir),
                    binversion=binversion,
                    ))


def ensure_one_match(query, matches, environments):
    """
    Checks envname query matches exactly one match.
    If matches zero, project list is printed.
    If matches >= 2, matching project list is printed.
    In both cases, program exists if validation fails.
    """

    # No Matches
    if not matches:
        msg = (
            "No matches for '{}'.\n"
            "Use 'poems --list' to see a list of available environments."
            "".format(query))
        click.echo(click.style(msg, fg='red'))
        sys.exit(0)

    # 2+ Matches
    elif len(matches) > 1:
        match = do_pick(environments=environments, query=query)
    # 1 Exact Match: Launch
    else:
        match = matches[0]

    return match


def ensure_project_dir_has_env(project_dir):
    output, code = call_poetry_env(project_dir)
    if code == 0:
        return output
    else:
        click.echo(click.style(output, fg='red'), err=True)
        sys.exit(1)


def ensure_valid_index(env_index, environments):
    if env_index not in range(0, len(environments)):
        raise click.UsageError('Invalid Environment Index')


def ensure_env_vars_are_ok(env_vars):
    error_msg = env_vars.validate_environment()
    if error_msg:
        click.echo(click.style(error_msg, fg='red'))
        sys.exit(1)


def ensure_poetry_config_is_ok(poetry_config):
    error_msg = poetry_config.validate()
    if error_msg:
        click.echo(click.style(error_msg, fg='red'))
        sys.exit(1)


def parse_new_poem_path(poem_path):
    if poem_path == ".":
        poem_path = os.path.abspath(os.getcwd())
    return poem_path


def ensure_path_exists(path):
    path_exists = os.path.exists(path)
    if not path_exists:
        error_msg = f"Path '{path}' does not exist."
        click.echo(click.style(error_msg, fg='yellow'))
        sys.exit(1)


def get_or_exit(output, code):
    if code == 0:
        return output
    else:
        click.echo(click.style(output, fg='red'), err=True)
        sys.exit(1)


if __name__ == '__main__':
    poems()
