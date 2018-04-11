# tidy-path
[![Releases](https://img.shields.io/github/release/jlinoff/tidy-path.svg?style=flat)](https://github.com/jlinoff/tidy-path/releases)

Bash script to remove all duplicates and, optionally undefined paths, from an environment variable like PATH.

Undefined paths will be removed if the -u option is specified.

It is typically installed like this.

```bash
$ git clone https://github.com/jlinoff/tidy-path.git
$ sudo cp tidy-path /usr/local/bin/
```

It is typically used like this.

```bash
$ PATH=$(tidy-path -u PATH)
```

It can also be used to list the components like this.

```bash
$ export TPATH="~/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/opt/path1:/opt/path2:/opt/path1:/usr/bin"
$ tidy-path -L TPATH
     1 0 ~/bin
     2 0 /usr/local/bin
     3 0 /usr/bin
     4 0 /bin
     5 0 /usr/sbin
     6 0 /sbin
     7 0 /opt/path1
     8 0 /opt/path2
     9 1 /opt/path1
    10 1 /usr/bin

Key
    0 - unique and defined
    1 - duplicate
    2 - undefined
    3 - undefined, duplicate

Summary
    Original Size : 10
    Final Size    : 8
    Removed       : 2
$ unset TPATH
```

Note that this tool only works with environment variables so locally
defined variables (without the export) keyword will not work unless
they prefix the command.

It is useful for tidying up environment variables that have lots of
duplicates from being set in various places. It can also help track
down the source of the duplicates.

The tool was written in bash so that it runs wherever bash runs.

These are the available options.

Short Option | Long Option  | Description
------------ | ------------ | ------------
-h | --help | Help message.
-l | --list | List the path data after filtering.
-L | --list-all | List all paths including the duplicate and undefined entries.
-u | --undefined | Filter out undefined paths or files. By default entries are treated as strings.
-V | --version | Print the program version and exit.

I have found surprisingly handy for reporting `PATH` and `LD_LIBRARY_PATH` settings in batch scripts.
