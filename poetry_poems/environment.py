# -*- coding: utf-8 -*-

""" Poems: Poetry Shell Switcher """

import os
import sys


class EnvVars():

    def __init__(self):
        self.IS_WINDOWS = sys.platform == 'win32'
        self.IS_MAC = sys.platform == 'darwin'
        self.IS_LINUX = sys.platform == 'linux'

        # self.HOME = os.getenv('HOME', '')

        self.POETRY_IS_ACTIVE = os.getenv('POETRY_ACTIVE')
        self.PIPENV_IS_ACTIVE = os.getenv('PIPENV_ACTIVE')
        self.VENV_IS_ACTIVE = os.getenv('VENV') or os.getenv('VIRTUAL_ENV')

        try:
            import curses  # noqa flake8
        except ImportError:
            self.HAS_CURSES = False
        else:
            self.HAS_CURSES = True

    def validate_environment(self):

        if False:
            pass
        # if self.POETRY_IS_ACTIVE:
        #     error = (
        #         "Poetry Shell is already active. \n"
        #         "Use 'exit' to close the shell before starting a new one.")

        elif self.PIPENV_IS_ACTIVE:
            error = (
                "Pipenv Shell is already active. \n"
                "Use 'exit' to close the shell before starting a new one.")

        # elif self.VENV_IS_ACTIVE:
        #     error = (
        #         "A Virtual environment is already active.\n"
        #         "Use 'deactivate' to close the enviroment "
        #         "before starting a new one.")

        else:
            return

        return error
