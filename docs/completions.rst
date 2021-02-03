================
Shell Completion
================

Autocomplete option is available because of a special ``--_completion`` flag, provided by the poems cli.
Below are instructions for setting up autocompletion for Bash, Zsh, Fish, and pdksh.

.. note::

    After setting the completions, please, remember to restart your session or open a new terminal ;)

.. warning::

    Autocompletin does not work when a virtualenv shell is already active.Make sure that you are not inside one before usage!

Bash + zsh
----------

Add the code below to your ``.bashrc/.zshrc``:

.. code:: console

    export BASE_SHELL=$(basename $SHELL)

    if [[ "$BASE_SHELL" == "zsh" ]] ; then
    autoload bashcompinit && bashcompinit
    fi

    _poetry_poems_completions() {
    COMPREPLY=($(compgen -W "$(poems --_completion)" -- "${COMP_WORDS[1]}"))
    }
    complete -F _poetry_poems_completions poems


Fish
----

Add a new file ``poems.fish`` to your Fish config folder (eg. ``~/.config/fish/completions/poems.fish``):

.. code:: console

    complete --command poems --arguments '(poems --_completion (commandline -cp))' --no-files

pdksh
-----

To have a shell completion, write into your personal ``~/.profile``, after the call of exported environments variables for your Python, as WORKON_HOME:

.. code:: console

    set -A complete_poems -- $(poems --_completion)


Credits
-------

`pipenv-pipes completions <https://pipenv-pipes.readthedocs.io/en/latest/completions.html>`_
