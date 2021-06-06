============
Installation
============

Compatibility
-------------

* Python 3.6+ (for Python 3.6 it may be necessary to run ``export LC_ALL=en_US.utf-8``)
* Ubuntu
* MacOS
* Windows10

  * Working in Command Prompt, PowerShell, Git Bash, `Cmder`_

  * For Git Bash invoking the tool may require prefixing the commands with ``winpty``. More reading: `git-for-windows`_, `winpty`_.

    .. code-block:: console

        $ winpty poems


Stable Release
--------------

To install most recent Poetry Poems version, run the following command in your terminal (MacOS + Ubuntu + Windows):

.. code-block:: console

    $ pip3 install poetry-poems

.. note::
    Poems requires the curses module, which is a part of the Python standard library and ready to use on Unix systems.
    However, curses module is not available on Windows. Therefore, Poems automatically installs `windows-curses <https://pypi.org/project/windows-curses/>`_ for Windows.


.. _Cmder: http://cmder.net/
.. _git-for-windows: https://github.com/git-for-windows/git/wiki/FAQ#some-native-console-programs-dont-work-when-run-from-git-bash-how-to-fix-it
.. _winpty: https://github.com/rprichard/winpty
