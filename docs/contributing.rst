##########################
Contributing & Development
##########################


Contributions are welcome and greatly appreciated!

How to Contribute
=================

Report Bugs
-----------

Report bugs at https://github.com/harper25/poetry-poems/issues


Fix Bugs
--------

Scan through the issues on GitHub. Please, feel free to implement a fix to any issue tagged with "bug" and "help wanted".


Implement Features
------------------

Scan through the issues on GitHub. Please, feel free to implement any feature tagged with "enhancement" and "help wanted".


Write Documentation
-------------------

Please, update the documentation after the bugfixes, new feature implementations and in any case when it is unclear, not detailed enough or outdated.


Submit Feedback
---------------

The best way to send feedback is to:

* Create a new issue at https://github.com/harper25/poetry-poems/issues
* Star the project :)

When you are proposing a new feature:

* Explain carefully your idea
* Keep the scope as narrow as possible, to make it easier to implement
* Consider involving youself in providing a solution :)


Setup Development Environment
=============================

Ready to contribute?
Here's how to set up Poems for local development.

1. Fork poetry-poems project on `GitHub <https://github.com/harper25/poetry-poems>`_.


2. Clone your fork locally:

    .. code:: console

        $ git clone git@github.com:YOUR_GITHUB_USERNAME/poetry-poems.git


3. Create a virtual environment with Poetry:

    .. code:: console

        $ cd poetry_poems
        $ poetry install
        $ poetry shell


4. Create a branch for local development so you can make your changes locally:

    .. code:: console

        $ git checkout -b issue-<issue-no>/<name-of-your-bugfix-or-feature>


5. Make sure that the code passes all tests after implementing changes. See the `Testing`_ section below for more details.

6. Commit your changes and push your branch to GitHub:

    .. code:: console

        $ git add .
        $ git commit -m "Short and meaningful commit message" -m "Detailed description of your changes."
        $ git push origin issue-<issue-no>/<name-of-your-bugfix-or-feature>

7. Submit a pull request through the GitHub website.


---------------

Testing
=======

Run unit tests
--------------

Unit tests are written in pytest.

.. code:: console

  $ pytest


Tox
---

It is possible to run the tests on all configured Python versions locally (it is also done in the CI pipeline). However, when using ``pyenv`` it is necessary to make them available to tox. It is possible by running:

.. code:: console

    $ pyenv local 3.6.9 3.7.5 3.8.3 3.9.0
    $ tox

.. note::

    Python versions have to be installed with Pyenv first:

    .. code:: console

        $ pyenv versions
        $ pyenv install --list
        $ pyenv install 3.6.9


Linter
------

The code is formatted with isort and black. Flake8 is used as a static linter.

.. code:: console

  $ isort .
  $ black .
  $ flake8 .


Pull Request Guidelines
=======================

Before submitting your pull request, please check if it meets these guidelines:

1. The pull request should contain tests that cover the new code (or decent amount).
2. The new functionalities should be described in the updated documentation.
3. The pull request should work for Python 3.6+. Please, check if the CI pipeline is passing: https://travis-ci.org/github/harper25/poetry-poems/pull_requests.


Deployment
==========

Reminder on how to release a new version:

* Bump a version in the project
* Push a tag to GitHub
* Release manually to PyPI
