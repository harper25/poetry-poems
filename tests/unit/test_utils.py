#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Tests for `poetry_poems` utils module."""

import os

import pytest

from poetry_poems.utils import (
    get_project_name,
    get_query_matches,
    collapse_path
)


@pytest.mark.utils
@pytest.mark.parametrize("folder_name,expected", [
    ("nonpoetryproject", None),
    ("project1-wXuP3rRk-py3.8", 'project1'),
    ("something-with-dash-edqXYkNx-py3.8", 'something-with-dash'),
])
def test_get_project_name(folder_name, expected):
    assert get_project_name(folder_name) == expected


@pytest.mark.utils
@pytest.mark.parametrize("query,num_results", [
    ("proj", 2),
    ("proj1", 1),
    ("o", 4),
    ("zzz", 0),
])
def test_get_query_matches(query, num_results, environments):
    rv = get_query_matches(environments, query)
    assert len(rv) == num_results


def test_collapse_path():
    home = os.path.expanduser("~")
    full_path = os.path.join(home, "filename")
    collapsed_path = collapse_path(full_path)

    assert home in full_path
    assert home not in collapsed_path
    assert "~" in collapsed_path
