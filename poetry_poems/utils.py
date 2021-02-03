# -*- coding: utf-8 -*-

""" Poems: Poetry Shell Switcher """

import os
import re


def get_project_name(folder_name):
    """ Returns name of a project given a Poetry Environment folder """
    POETRY_FOLDER_PAT = r"^(.+)-[\w_-]{8}-py[2-9].[0-9]+$"  # noqa: FS003
    match = re.search(POETRY_FOLDER_PAT, folder_name)
    return None if not match else match.group(1)


def get_query_matches(environments, query):
    """ Returns matching environments from an Environment list and a query """
    matches = []
    for environment in environments:
        if query.lower() in environment.envname.lower():
            matches.append(environment)
    return matches


def collapse_path(path):
    """ Replaces Home value in a path for its variable name """
    home = os.path.expanduser("~")
    path = path.replace(home, "~")
    return path


def parse_new_poem_path(poem_path):
    if poem_path == ".":
        poem_path = os.path.abspath(os.getcwd())
    return poem_path
