#!/usr/bin/env python
'''
Tidy up shell paths by removing duplicates entries and, optionally,
undefined paths.

It is very useful keeping your shell path environment variables
tidy. Here is an example usage:

    $ PATH=$(tidypath.py PATH)

It can also be used to list path information in a readable way:

    $ tidypath.py -l PATH

Note that this tool only works with environment variables so locally
defined variables (defined without the export keyword) will not work
unless they are are part of the command.

For example, this works:

    $ # This works.
    $ YPATH="${PATH}:${PATH}" tidypath.py -L -u YPATH

This also works.

    $ # This works.
    $ export YPATH="${PATH}:${PATH}"
    $ tidypath.py -L -u YPATH
        $ unset YPATH

But this does not.

    $ # This does not work, YPATH is a local variable.
    $ YPATH="${PATH}:${PATH}"
    $ tidypath.py -L -u YPATH

It was written in python and is compatible with py2 and py3.
'''
from __future__ import print_function
import argparse
import inspect
import os
import sys


__version__ = '1.0.0'


def err(msg, level=1, exit_code=1, out=sys.stderr):
    '''
    Print an error message and exit.
    '''
    w = out.write
    w('\033[31;1m')
    w('ERROR:')
    w('{}:'.format(inspect.stack()[level][2]))
    w('\033[0;31m')
    w(' {}'.format(msg))
    w('\033[0m')
    w('\n')
    sys.exit(exit_code)


def get_canon(comp):
    '''
    Return the canonical path name.
    '''
    return os.path.abspath(os.path.expanduser(comp))


def is_dup(dups, comp):
    '''
        Use canonical form to eliminate duplicates.
        This works even if the path does not exist.
        '''
    canon = get_canon(comp)
    if canon in dups:
        return True
    dups[canon] = True
    return False


def exists(comp):
    '''
        Report if this is undefined.
        '''
    canon = get_canon(comp)
    return os.path.exists(canon)


def report(opts, comps, env):
    '''
    Report the path information (-L).
    '''
    print('Name: {}'.format(env))
    dups = {}
    numu = 0
    numd = 0
    numf = 0
    numk = 0

    if opts.color:
        crb = '\033[31;1m'  # red-bold
        cgb = '\033[32;1m'  # green-bold
        crs = '\033[0m'     # clear/reset
        if opts.undefined:
            cuc = crb
        else:
            cuc = cgb
    else:
        crb = ''
        cgb = ''
        crs = ''
        cuc = ''

    wri = sys.stdout.write
    for i, comp in enumerate(comps, start=1):
        wri('{:>4}'.format(i))

        kept = False  # avoid double counting
        if is_dup(dups, comp):
            wri(' {}d{}'.format(crb, crs))
            numd += 1
            numf += 1
        else:
            wri(' {}u{}'.format(cgb, crs))
            kept = True

        if exists(comp):
            wri('{}e{}'.format(cgb, crs))
            kept = True
        else:
            numu += 1
            if opts.undefined:
                numf += 1
            wri('{}n{}'.format(cuc, crs))

        if kept:
            numk += 1

        wri(' {}'.format(comp))
        wri('\n')

    print('''
Key:
     {6}u{4}{6}e   {6}u{4}nique, {6}e{4}xists
     {5}d{4}{6}e   {5}d{4}uplicate, {6}e{4}xists
     {6}u{4}{7}n   {6}u{4}nique, does {7}n{4}ot exist
     {5}d{4}{7}n   {5}d{4}uplicate, does {7}n{4}ot exist

Summary:
    Num Kept       : {0:>2}
    Num Filtered   : {1:>2}
    Num Duplicates : {2:>2}
    Num Undefined  : {3:>2}\
'''.format(numk, numf, numd, numu, crs, crb, cgb, cuc))


def process(opts, env):
    '''
    Analyze the contents of a path environment variable.
    '''
    if env not in os.environ:
        if opts.silent is False:
            err('environment variable not defined: {}, use -s to continue'.format(env))
        else:
            comps = []
    else:
        comps = os.environ[env].split(os.pathsep)

    if opts.list_report:
        report(opts, comps, env)
        return

    new_comps = []
    dups = {}
    for comp in comps:
        if is_dup(dups, comp):
            continue

        # Filter out undefined components if the user
        # told us to.
        if opts.undefined and not exists(comp):
            continue

        # This is a keeper. Maintain relative order.
        new_comps.append(comp)

    if opts.list:
        for i, comp in enumerate(comps, start=1):
            print('{:>2} {}'.format(i, comp))
    else:
        print(os.pathsep.join(new_comps))


def getopts():
    '''
    Command line options.
    '''
    def gettext(s):
        '''
        Convert to upper case to make things consistent.
        '''
        lookup = {
            'usage: ': 'USAGE:',
            'positional arguments': 'POSITIONAL ARGUMENTS',
            'optional arguments': 'OPTIONAL ARGUMENTS',
            'show this help message and exit': 'Show this help message and exit.\n ',
        }
        return lookup.get(s, s)

    argparse._ = gettext  # to capitalize help headers
    base = os.path.basename(sys.argv[0])
    #name = os.path.splitext(base)[0]
    usage = '\n  {0} [OPTIONS] [ENV_VARS]'.format(base)
    desc = 'DESCRIPTION:{0}'.format('\n  '.join(__doc__.split('\n')))
    epilog = r'''
EXAMPLES:
   # Example 1: help
   $ {0} -h

   # Example 2: clean a path (remove duplicates)
   $ {0} PATH

   # Example 3: clean a path (remove duplicates and undefined)
   $ {0} -u PATH

   # Example 4: list path contents
   $ {0} -l PATH

   # Example 5: list path contents with undefined entries removed.
   $ {0} -lu PATH

   # Example 6: clean up PATH and LD_LIBRARY_PATH
   export PATH=$({0} PATH)
   export LD_LIBRARY_PATH=$({0} LD_LIBRARY_PATH)

   # Example 7: report the path information for PATH and
   #            LD_LIBRARY_PATH
   $ {0} -L PATH LD_LIBRARY_PATH

   # Example 8: report path information with a bit of color.
   $ {0} -Lc PATH

   # Example 9: Set an environment variable and guarantee
   #            that it works when the variable is not
   #            defined.
   $ export LD_LIBRARY_PATH=$({0} -s LD_LIBRARY_PATH)

VERSION
   {0} {1}

PROJECT
   https://github.com/jlinoff/tidy-path

LICENSE
   Copyright (c) 2018 by Joe Linoff
   MIT Open Source
'''.format(base, __version__)
    afc = argparse.RawTextHelpFormatter
    parser = argparse.ArgumentParser(formatter_class=afc,
                                     description=desc[:-2],
                                     usage=usage,
                                     epilog=epilog.rstrip() + '\n ')

    parser.add_argument('-c', '--color',
                        action='store_true',
                        help='''\
Add some color cues.
 ''')

    parser.add_argument('-l', '--list',
                        action='store_true',
                        help='''\
List the path contents in human readable form.
The default is to list them in shell form.
 ''')

    parser.add_argument('-L', '--list-report',
                        action='store_true',
                        help='''\
List current state of the path variable as a
report with no filtering.
 ''')

    parser.add_argument('-s', '--silent',
                        action='store_true',
                        help='''\
Fail silently. This is useful for gracefully
handling environment variables that are not
defined.

Here is an example:
    {0} -L NOT_DEFINED
 '''.format(base))    
    parser.add_argument('-u', '--undefined',
                        action='store_true',
                        help='''\
Remove undefined entries or show undefined entries
if -L is specified.

This is optional because there often times when
it may be desirable to specify undefined paths
in anticipation of the path being created later.
 ''')

    parser.add_argument('-V', '--version',
                        action='version',
                        version='%(prog)s version {0}'.format(__version__),
                        help='''\
Show program's version number and exit.
 ''')

    parser.add_argument('ENV_VARS',
                        nargs='*',
                        help='''\
One or more environment variable names like PATH, MANPATH or
LD_LIBRARYP_PATH.
 ''')
    opts = parser.parse_args()
    return opts


def main():
    opts = getopts()
    for env in opts.ENV_VARS:
        process(opts, env)


if __name__ == '__main__':
    main()
