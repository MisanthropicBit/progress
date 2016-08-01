**progress v1.3.0**
===================

.. image:: https://travis-ci.org/MisanthropicBit/progress.svg?branch=master
.. image:: https://coveralls.io/repos/github/MisanthropicBit/progress/badge.svg?branch=master
   :target: https://coveralls.io/github/MisanthropicBit/progress?branch=master
.. image:: https://img.shields.io/pypi/v/progress2.svg?maxAge=2592000
.. image:: https://img.shields.io/pypi/l/progress2.svg?maxAge=2592000

Allows for easy creation of progress-bars and text.

``progress`` has been tested with Python 2.6, 2.7, 3.2, 3.3 and PyPy, and as of now requires at least Python 2.6

Installation:
-------------
**Note:** PyPI already contains a ``progress`` entry, so this module is located
at `progress2 <https://pypi.python.org/pypi/progress2>`_.

You can install via `pip <https://pip.pypa.io/en/latest/>`_::

    pip install progress2

Alternatively, download the source files and run the following command from the
download directory::

    python setup.py install

Usage:
------

Creating a ``ProgressBar``:

    >>> import progress
    >>> bar = progress.ProgressBar("[{progress}] {percentage:.2f}% ({minutes}:{seconds})", width=30)
    >>> bar.show()
    [                              ] 0.00% (0:0)>>>
    >>> bar.update(26)
    >>> bar.show()
    [======>                       ] 26.00% (0:0)>>>
    >>>

Alternatively, you can use the ``autoupdate`` method:

    >>> bar.autoupdate(42)
    [===================>          ] 68.00% (0:45)>>>
    >>>

Creating a ``ProgressText``:

    >>> text = progress.ProgressText("Searching: {progress}", "|/-\\", autoreset=True)
    >>> text.show()
    |>>>
    >>> text.update(); text.show()
    />>>
    >>> text.update(); text.show()
    ->>>
    >>> text.update(); text.show()
    \>>>

You can supply custom args and kwargs to ``show`` and ``autoupdate``:

    >>> bar = progress.ProgressBar("[{progress}] {key} {},{},{}")
    >>> d = dict(key=33)
    >>> l = range(3)
    >>> bar.update(50)
    >>> bar.show(*l, **d)
    [=========>          ] 33 0,1,2>>>
    >>> bar.autoupdate(25, *l, **d)
    [==============>     ] 33 0,1,2>>>
    >>>

Refer to the ``examples/`` directory for more examples. There are also examples
of how to use ``progress`` with the ``threading`` module.

Implementation Notes:
---------------------

Since most terminals cannot clear their output buffers across newlines or carriage returns,
``progress`` does not work if you insert them, e.g. ``progress.ProgressBar("{progress}\n{percentage}")``
will not be cleared from the terminal.
