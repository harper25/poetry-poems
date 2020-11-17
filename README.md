# Poems

Poetry Environment Switcher

[![Build Status](https://travis-ci.org/harper25/poetry-poems.svg?branch=master)](https://travis-ci.org/harper25/poetry-poems)
[![codecov](https://codecov.io/gh/harper25/poetry-poems/branch/master/graph/badge.svg)](https://codecov.io/gh/harper25/poetry-poems)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

--------

Overview
--------

Poetry-poems is a tool that speeds up switching between Poetry projects by navigating to a specific Poetry project and activating Poetry shell at the same time.

Supported OS:
- [x] Mac OS
- [x] Linux
- [x] Windows 10

![poems-intro](https://github.com/harper25/poetry-poems/blob/master/docs/static/poems-intro.gif)

Documentation
-------------

Virtual environments created with Poetry (`poetry shell`), by default kept in `poetry config virtualenvs.path`, do not store paths to projects that use them. The only link available points from a project directory to a corresponding Poetry virtual environment. Therefore, a hidden file `.poetry-poems` placed in `$HOME` is created to store paths to Poetry projects.

Before running poetry-poems you have to add Poetry project paths to the poems file:
```sh
poems --add <project_path>
poems --add $PWD
poems --add .
```

It is possible to use a different file then default `$HOME/.poetry-poems`:
```sh
poems --poems_file <custom_poems_file> --add <project_path>
```

In case you would like to save a project with a virtual environment located in the project directory (created with `virtualenv` or `python -m venv`), please ensure that Poetry is configured correctly in the project directory:
```sh
cd <project_path>
poetry env list --full-path
poetry config --local virtualenvs.in-project true
```

Choose a project to launch in an interactive mode:
```sh
poems
```

Launch a specific project:
```sh
poems <envname>
```

List all saved projects:
```sh
poems --list
poems --list --verbose
```

Delete a project path from poems file:
```sh
poems --delete
poems --delete envname
```

### Completions

After setting the completions, please, restart your session or open a new terminal ;)

**Bash + zsh**

Add the code below to your .bashrc/.zshrc:
```sh
export BASE_SHELL=$(basename $SHELL)

if [[ "$BASE_SHELL" == "zsh" ]] ; then
autoload bashcompinit && bashcompinit
fi

_poetry_poems_completions() {
COMPREPLY=($(compgen -W "$(poems --_completion)" -- "${COMP_WORDS[1]}"))
}
complete -F _poetry_poems_completions poems
```

**Fish**

Add a new file poems.fish to your Fish config folder (eg. ~/.config/fish/completions/poems.fish):

```sh
complete --command poems --arguments '(poems --_completion (commandline -cp))' --no-files
```

**pdksh**

To have a shell completion, write into your personal ~/.profile, after the call of exported environments variables for your Python, as WORKON_HOME:

```sh
set -A complete_poems -- $(poems --_completion)
```

### Tox

When using `pyenv` it is necessary to make certain python versions available to tox. It is possible by invoking (the versions have to be installed first):
```sh
pyenv versions
pyenv install --list
pyenv install 3.6.9
pyenv local 3.6.9 3.7.5 3.8.3 3.9.0
```

### TODO

Still a lot [TODO](https://github.com/harper25/poetry-poems/blob/master/TODO.md)

License
-------

[MIT License](https://github.com/harper25/poetry-poems/blob/master/LICENSE)

Credits
-------

Project based on [Pipes](https://github.com/gtalarico/pipenv-pipes), Pipenv Environment Switcher ⚡.

A modified version of [Pick](https://github.com/wong2/pick/) for curses based interactive selection list in the terminal is also used.

Author
------

[harper25](https://github.com/harper25)
