# Poems

Poetry Environment Switcher

--------

Overview
--------

Poetry-poems is a tool that speeds up switching between Poetry projects by navigating to a specific Poetry project and activating Poetry shell at the same time.

Documentation
-------------

Virtual environments created with Poetry (`poetry shell`), by default kept in `poetry config virtualenvs.path`, do not store paths to projects that use them. The only link available points from a project directory to a corresponding Poetry virtual environment. Therefore, a hidden file `.poetry-poems` placed in `$HOME` is created to store paths to Poetry projects.

Before running poetry-poems you have to add Poetry project paths to the poems file:
```python
poems --add <project_path>
poems --add $PWD
poems --add .
```

It is possible to use a different file then default `$HOME/.poetry-poems`:
```python
poems --poems_file <custom_poems_file> --add <project_path>
```

In case you would like to save a project with a virtual environment located in the project directory (created with `virtualenv` or `python -m venv`), please ensure that Poetry is configured correctly in the project directory:
```python
cd <project_path>
poetry env list --full-path
poetry config --local virtualenvs.in-project true
```

Choose a project to launch in an interactive mode:
```python
poems
```

Launch a specific project:
```python
poems <envname>
```

List all saved projects:
```python
poems --list
poems --list --verbose
```

Delete a project path from poems file:
```python
poems --delete
poems --delete envname
```

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
