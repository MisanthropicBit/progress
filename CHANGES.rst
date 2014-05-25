Version log
===========

0.1.0
-----

- Initial version

0.2.0
-----

- Added ``SimpleETA``, ``SMAETA`` and ``EMAETA`` convenience classes
- Reimplemented the ``ETA`` calculation method to use an
  ``ETA`` base class through the ``etaobj`` parameter

0.2.1
-----

- Renamed ``progress.Colorizer`` to ``progress.BaseColorizer`` and
  platform-specific color manager classes to ``Colorizer`` to
  standardize naming convention
- Added classmethod format to ``BaseColorizer``
- Removed synchronized update from ``ProgressBar`` class
- Reformatted ``ProgressBar`` constructor
- Removed ``unit`` format string
- Minor ``color_code`` clean-up
- Finished ``ETA`` classes (untested)
- Cleaned up in ``progress/__init__.py``

0.2.2
-----

- Fixed bugs in ``ProgressBar`` constructor
- Moved ``parse_cc`` into ``BaseColorizer`` and added ``parse_cc_all`` and ``__COLOR_CODE_RE``
- Fixed bugs in ``parse_cc``

0.3.2
-----

- Rewrote the ``ProgressBar`` class to use Python 2.6+ string formatting
  instead of '%' formatting
- Replaced ``frac1`` and ``frac2`` with ``nominator`` and ``denominator``
- Replaced ``eta`` argument with ``hours``, ``minutes`` and ``seconds``

0.3.3
-----

- Fixed a bug in ``ProgressBar.__update`` where the current line would not
  be overriden correctly
- ETA objects can now return an int/float in seconds or a tuple/list of hours, minutes and seconds
- Changed update code to account for ``char``/``head`` being longer than 1

0.3.4
-----

- Added the ``ColorFormatter`` class for extracting color markup syntax from format strings
- Added docstrings, ``__version__`` and ``__date__`` for all files
- Added the ``ProgressText`` class
- Added the ``progress.color`` submodule containing string coloring tools
- Changed ``__date__`` formats from DD-MM-YYYY to YYYY-MM-DD
- Updated main module docstring

0.3.5
-----

- Added inherit_docstrings decorator to ``progress/__init__.py``
- Removed ``__version__`` attributes from all files but ``progress/__init__.py``
- Changed ``ColorFormatter``'s parse return value to resemble ``string.Formatter``'s return value
- Moved version log into a separate file
- Created a ``README.rst`` file for github
- Refactored ``progress.color.cprint`` to use less code
- Fixed some relative imports
- Cleaned up some code in ``nix.ColorManager`` and ``win.ColorManager``
- Removed all if ``__name__ == '__main__'``... tests
- Added missing ``__date__`` attribute to ``BaseColorManager.py``

0.4.0
-----

- Added ``__len__`` to ``ProgressBar``
- Refactored entire module layout
- Moved most innards of ``progress/__init__.py`` into ``progress.color``
- Moved platform-specific color managers under ``color/`` and ``ProgressBar.py`` and ``ProgressText.py``
  to be under the top-level package
- Removed some unused imports
- Added ``DummyColorManager`` class for when color is not supported (instead of raising)
- Added ``color_supported`` function to ``color/__init__.py``
- Moved ``inherit_docstrings`` decorator into ``decorators.py`` at top-level

0.4.1
-----

- Fixed some bugs in ``ColorFormatter.parse``, ``cprint`` and ``win.ColorManager.set_color`` (``cprint`` now
  throws ``ValueError`` instead of ``RuntimeError``, and the latter now properly resets console colors)
- Changed docstrings for ``ProgressBar.py`` and ``ProgressText.py`` to reflect that they are not platform-specific
  anymore
- Updated docstrings in eta directory to conform to PEP8
- Removed ``None`` and ``''`` keys from ``win.ColorManager`` color dict
- Removed ``render_text`` method from all color managers
- Fixed a bug in ``cprint`` when multiple color syntaxes were present
- Added ``target`` (stream) parameter to ``set_defaults`` (color managers) to ensure defaults are set for the
  appropriate stream
- Added ``has_colors`` and ``has_custom_colors`` to color managers
- Changed all relative imports to absolute
- Fixed a bug in ``ProgressBar.clear`` and ``ProgressText.clear``
- Removed ``CursesColorManager`` since curses is not fitting for coloring (removes content from screen etc.)
- Renamed ``ANSIColorManager`` to ``ColorManager``
- ``win.ColorManager._onerror`` now properly frees the error message buffer
- Fixed a serious bug with the ``SYS_FLAG`` binary flag in ``win.ColorManager``
- Added some additional error checking
- Added docstring to ``decorators.py``
- Added stuff to ``compat.py`` and updated some of the code for Python 3+
- cprint now flushes its target file which caused colors to not work with Python 3+
- Added ``custom_colors_supported`` function in ``color/__init__.py``
- Foreground- and background colors now properly default to their respective defaults if not present in
  ``win.ColorManager.set_color``
- Minor code clean-up in ``ProgressBar.py``
- Added ``progress.color`` to ``ProgressBar.py`` and added support for colored progress
- Minor clean-up in ``ProgressBar.clear``
- Fixed bug in ``ColorFormatter.py``

1.0.0
-----

- **MAJOR CHANGE**: Moved ``progress.color`` and everything related out of the main project due to
  unforseen complications with the submodule. It will be merged into a separate module called
  ``colorise`` at a later date.
- All code now conforms to PEP8 and PEP275
- Updated and shortened various docstrings
- Renamed version_log.txt (this file) to VERSION_LOG.rst and put all changes into bulleted lists
- Changed ``setup.py`` to reflect the above major change
- Added ``__date__`` to ``eta/`` files
- Added ``MANIFEST.in`` file to project
- Minor changes in ``eta/SimpleETA`` to reflect intention of derived methods
- Removed ``ProgressBar.__update`` since its original purpose is now obsolete
- Fixed an exception message typo in ``ProgressBar.py``
- Changed all members in ``ProgressBar`` and ``ProgressText`` to use a single underscore instead of a double underscore,
  made some "private" members public and removed the ``value``, ``set`` and ``percentage`` methods
  (since the member variables are now public)
- Removed ``__update_fmtdict`` from ``ProgressBar`` and moved ``__format_eta`` into ``progress.eta.BaseETA`` and renamed
  it to ``format_eta``
- Added ``__date__``'s to ``compat.py`` and ``decorators.py``
- Fixed a bug in ProgressBar.update where the width would not remain constant due to a rounding error
- Removed check for invalid format field names, since Python complains fine on its own
- Added a check to ensure ``char`` and ``head`` are both length 1

1.1.0
-----
- Renamed ``VERSION_LOG.rst`` to ``CHANGES.rst``
- Fixed a bug in the ``ProgressBar`` constructor
- ``ProgressBar`` now raises an exception if an ``etaobj`` is given without the eta format
- Fixed a small bug in the ``reset`` method
- Allowed the ``head`` keyword in the ``ProgressBar`` constructor to be empty
- Added some properties to ``ProgressBar``
- ``ProgressText`` now clear the entire progress before restarting when ``autoreset == False``
- Updated examples/ and added ``threaded_progress_bar.py`` and ``threaded_progress_text.py``
- Updated test cases
- Updated error checking in ``ProgressText`` constructor
- Added new properties, which now all changes the ProgressBar's state accordingly
