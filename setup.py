"""progress module setup script for distribution."""

from __future__ import with_statement
import distutils.core


def get_version(filename):
    with open(filename) as fh:
        for line in fh:
            if line.startswith('__version__'):
                return line.split('=')[-1].strip()[1:-1]


distutils.core.setup(
    name='progress',
    version=get_version('./progress/__init__.py'),
    author='Alexander Bock',
    author_email='alexander.asp.bock@gmail.com',
    platforms='Platform independent',
    description=('Allows for easy creation of progress-bars and text'),
    license='MIT',
    keywords='progress, progressbar, progresstext',
    url='https://github.com/MisanthropicBit/progress',
    packages=['progress', 'progress.eta'],
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
