# stowage

![stowage badge](https://badge.fury.io/py/stowage.png)

![travis badge](https://travis-ci.org/michaelpb/stowage.png?branch=master)

Stow-like designed for keeping dotfiles under version control, written in python


## Installation

Assuming Python's `pip` is installed (for Debian-based systems, this can be
installed with `sudo apt-get install python-pip`), stowage can be installed
directly from PyPI:

```
pip install stowage
```

Python versions 3.3+ (and 2.6+) are supported and tested against.

## Quick start

1. Setup your dotfiles repo (by default `stowage` assumes its at `~/dotfiles`,
but it could be anywhere)

```
mkdir ~/dotfiles
cd ~/dotfiles
git init
```

2. Create one or more dotfile 'packages'

```
# An example, making one for your .vimrc
# Notice that we can call it _vimrc instead of .vimrc, making it visible /
# easier to interact with
mkdir ~/dotfiles/vim
cp ~/.vimrc ~/dotfiles/vim/_vimrc
```
3. Activate `stowage`

```
stowage vim
```

Now, your `~/.vimrc` has been replaced by a symlink to the
`~/dotfiles/vim/_vimrc` file, enabling the `~/dotfiles` directory to be more
easily put into version control.

## Full usage

```
usage: stowage [-h] [-n] [-v] [-s SOURCE] [-d DESTINATION] [-b BACKUP] [-B]
               [packages [packages ...]]

Symlink files recursively, good for dotfiles.

positional arguments:
  packages              one or more packages

optional arguments:
  -h, --help            show this help message and exit
  -n, --dryrun          dryrun, just simulate
  -v, --verbose         increase output verbosity
  -s SOURCE, --source SOURCE
                        stowage source directory
  -d DESTINATION, --destination DESTINATION
                        stowage destination directory
  -b BACKUP, --backup BACKUP
                        stowage backup directory
  -B, --skip-backup     skip making backups
```

# Contributing

New features, tests, and bug fixes are welcome!
