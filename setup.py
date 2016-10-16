"""progress module setup script for distribution."""

from __future__ import with_statement

import os
import distutils.core


def get_version(filename):
    with open(filename) as fh:
        for line in fh:
            if line.startswith('__version__'):
                return line.split('=')[-1].strip()[1:-1]


distutils.core.setup(
    name='progress2',
    version=get_version(os.path.join('progress', '__init__.py')),
    author='Alexander Bock',
    author_email='alexander.asp.bock@gmail.com',
    platforms='All',
    description=('Allows for easy creation of progress-bars and text'),
    license='MIT',
    keywords='progress, progressbar, progresstext',
    url='https://github.com/MisanthropicBit/progress',
    packages=['progress', 'progress.eta'],
    package_data={'progress': ['examples/*.py', 'tests/*.py']},
    long_description=open('README.rst').read(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'Topic :: Terminals',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3'
    ]
)
