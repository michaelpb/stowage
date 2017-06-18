import argparse
import os
import sys

_is_verbose = False
parser = None


class ArgError(ValueError):
    pass


def parse_args(argv):
    global parser
    parser = argparse.ArgumentParser(
        prog='stowage',
        description='Symlink files recursively, good for dotfiles.'
    )

    backup_dir = os.environ.get('STOWAGE_BACKUP', '~/.config/stowage/backup/')
    destination_dir = os.environ.get('STOWAGE_DESTINATION', '~')
    source_dir = os.environ.get('STOWAGE_SOURCE', '~/dotfiles')

    parser.add_argument('-n', '--dryrun', help='dryrun, just simulate',
                        action='store_true')
    parser.add_argument('-v', '--verbose', help='increase output verbosity',
                        action='store_true')
    parser.add_argument('-s', '--source', help='source directory',
                        default=source_dir)
    parser.add_argument('-d', '--destination', help='destination directory',
                        default=destination_dir)
    parser.add_argument('-b', '--backup', help='backup directory',
                        default=backup_dir)
    parser.add_argument('-B', '--skip-backup', help='skip making backups',
                        action='store_true')
    parser.add_argument('packages', nargs='*', help='one or more packages')
    return parser.parse_args(argv)


def source_directories(args):
    '''
    Given parsed args, yield paths to all source directories
    '''
    for package_name in args.packages:
        yield os.path.join(args.source, package_name)


def munge_path(path):
    '''
    Replaces all files prefixed with '_' with ones prefixed with '.'
    '''
    return os.path.join(*[
        node if not node.startswith('_') else '.%s' % node[1:]
        for node in os.path.split(path)
    ])


def directory_walk(source_d, destination_d):
    '''
    Walk a directory structure and yield full parallel source and destination
    files, munging filenames as necessary
    '''
    for dirpath, dirnames, filenames in os.walk(source_d):
        relpath = os.path.relpath(dirpath, source_d).strip('./')
        for filename in filenames:
            suffix = filename
            if relpath:
                suffix = os.path.join(relpath, filename)
            full_source_path = os.path.join(source_d, suffix)
            full_destination_path = os.path.join(
                destination_d, munge_path(suffix))
            yield full_source_path, full_destination_path


def needed_symlink_walk(source_d, destination_d):
    '''
    Given a destination directory, walk through a source direct yielding all
    paths that need symlinks, to make the destination resemble the source
    '''
    for source, destination in directory_walk(source_d, destination_d):
        if os.path.islink(destination):
            # Should doublecheck if is symlink to source
            continue
        yield source, destination


def check_args(args):
    '''
    Raises value errors if args is missing something
    '''
    if not args.packages:
        raise ArgError()
    if args.verbose:
        global _is_verbose
        _is_verbose = True
    # Expand all relevant user directories
    args.source = os.path.expanduser(args.source)
    args.destination = os.path.expanduser(args.destination)
    args.backup = os.path.expanduser(args.backup)


def get_backup_path(args, destination):
    '''
    Given parsed args, generates the full backup path for the destination file
    '''
    relpath = os.path.relpath(args.destination, destination).strip('./')
    fullpath = os.path.join(args.backup, relpath)
    backup_path = fullpath
    tries = 0
    while os.path.exists(backup_path) and tries < 10:
        backup_path = '%s.%i' % (fullpath, tries)
        if _is_verbose:
            print('Backup path exists, trying %s' % backup_path)
        tries += 1
    return backup_path


def do_backup(destination, backup_path):
    try:
        os.makedirs(os.path.dirname(backup_path))
    except OSError:
        pass
    os.rename(destination, backup_path)


def do_symlink(source, destination):
    try:
        os.makedirs(os.path.dirname(destination))
    except OSError:
        pass
    os.symlink(source, destination)


def main(args):
    try:
        check_args(args)
    except ArgError:
        parser.print_help()
        sys.exit(1)

    # Args are correct, lets now perform necessary steps
    for source_d in source_directories(args):
        needed_symlinks = needed_symlink_walk(source_d, args.destination)
        for source, destination in needed_symlinks:
            # Backup logic
            if not args.skip_backup and os.path.exists(destination):
                backup_path = get_backup_path(args, destination)
                if _is_verbose:
                    message_tmpl = 'Backing up {0} -> {1}'
                    print(message_tmpl.format(destination, backup_path))
                do_backup(destination, backup_path)

            # Symlink and dryrun logic
            if _is_verbose or args.dryrun:
                print('{0} -> {1}'.format(source, destination))
            if not args.dryrun:
                do_symlink(source, destination)


def cli():
    main(parse_args(sys.argv))


if __name__ == '__main__':
    cli()
