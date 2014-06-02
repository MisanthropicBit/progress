**progress v1.1.0**
=================================

.. image:: https://travis-ci.org/MisanthropicBit/progress.svg?branch=master
    :target: https://travis-ci.org/MisanthropicBit/progress

.. image:: https://pypip.in/license/progress2/badge.png
    :target: https://pypi.python.org/pypi/progress2/

Allows for easy creation of progress-bars and text.

``progress`` has been tested with Python 2.6, 2.7, 3.2 and 3.3, and as of now requires at least Python 2.6

Installation:
-------------
**Note:** PyPI already contains a ``progress`` entry, so this module is located
at `progress2 <https://pypi.python.org/pypi/progress2>`_.

You can install via `pip <https://pip.pypa.io/en/latest/>`_::

    pip install progress2

Alternatively, if you downloaded the source files, just run the following command from the
download directory::

    python setup.py install

Usage:
------

Creating a ``ProgressBar``:

.. code::

    >>> import progress
    >>> bar = progress.ProgressBar("[{progress}] {percentage:.2f}% ({minutes}:{seconds})", width=30)
    >>> bar.show()
    [                              ] 0.00% (0:0)>>>
    >>> bar.update(26)
    >>> bar.show()
    [======>                       ] 26.00% (0:0)>>>
    >>>

Creating a ``ProgressText``:

.. code::

    >>> text = progress.ProgressText("Searching: {progress}", "|/-\\", autoreset=True)
    >>> text.show()
    |>>>
    >>> text.update(); text.show()
    />>>
    >>> text.update(); text.show()
    ->>>
    >>> text.update(); text.show()
    \>>>

Refer to the ``examples/`` directory for some example code.

Implementation Notes:
---------------------

Since most terminals cannot clear their output buffers across newlines or carriage returns,
``progress`` does not work if you insert them, e.g. ``progress.ProgressBar("{progress}\n{percentage}")``
will not be cleared from the terminal.
