#!/usr/bin/env python

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()


try:
    import pypandoc
except ImportError:
    print('Cannot release without pypandoc installed. '
          'Used to translate from Markdown to Re-Structured Text.')
    sys.exit(1)

readme = pypandoc.convert('README.md', 'rst')

# doclink = """
# Documentation
# -------------
#
# The full documentation is at http://stowage.rtfd.org."""
# history = open('HISTORY').read().replace('.. :changelog:', '')
doclink = ''
history = ''

setup(
    name='stowage',
    version='0.1.7',
    description='Stow-like application for keeping '
                'your dot-files under version control',
    long_description=readme + '\n\n' + doclink + '\n\n' + history,
    author='michaelb',
    author_email='michaelpb@gmail.com',
    url='https://github.com/michaelpb/stowage',
    packages=[
        'stowage',
    ],
    entry_points={
        'console_scripts': ['stowage=stowage.stowage:cli'],
    },
    package_dir={'stowage': 'stowage'},
    install_requires=[],
    license='GPL3',
    keywords='stowage',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        "Environment :: Console",
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: PyPy',
        'License :: OSI Approved :: '
        'GNU General Public License v3 or later (GPLv3+)',
    ],
)
