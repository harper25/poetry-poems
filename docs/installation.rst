============
Installation
============

Compatibility
-------------

* Python 3.6+ (for Python 3.6 it may be necessary to run ``export LC_ALL=en_US.utf-8``)
* Unix + Windows (tested on Win10)

Stable Release
--------------

To install most recent Poetry Poems version, run the following command in your terminal (MacOs + Ubuntu + Windows):

.. code-block:: console

    $ pip3 install poetry-poems

.. note::
    Poems requires the curses module, which is a part of the Python standard library and ready to use on Unix systems.
    However, curses module is not available on Windows. Therefore, Poems automatically installs `windows-curses <https://pypi.org/project/windows-curses/>`_ for Windows.

Terminal
~~~~~~~~

While Poetry Poems should work on the standard Windows console (cmd.exe)
a terminal like `Cmder`_ is highly recommended:

.. _Cmder: http://cmder.net/
