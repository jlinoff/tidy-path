# tidy-path
Bash script to remove all duplicates and, optionally undefined paths, from an environment variable like PATH.

Undefined paths will be removed if the -u option is specified.

It is typically used like this.

```bash
$ PATH=$(tidy-path.sh -u PATH)
```

It can also be used to list the variable entries.

```bash
$ export TEST_PATH="${PATH}:${PATH}:/undef/dir1:/undef/dir2:/undef/dir2"
$ tidy-path.sh -L -u TEST_PATH
.
.
```

Note that this tool only works with environment variables so locally defined variables (without the export)
keyword will not work unless they are are part of the command.

It tool is useful for tidying up environment variables that have lots of duplicates.
It can also help track down the source of the duplicates.

It was written in bash so that it runs wherever bash runs.

These are the available options.

Short Option | Long Option  | Description
------------ | ------------ | ------------
-h | --help | Help message.
-l | --list | List the path data after filtering.
-L | --list-all | List all paths including the duplicate and undefined entries.
-u | --undefined | Filter out undefined paths or files. By default entries are treated as strings.
-V | --version | Print the program version and exit.

I have found surprisingly handy for reporting `PATH` and `LD_LIBRARY_PATH` settings in batch scripts.
